from typing import Iterable, Callable
from functools import partial

from django.conf import settings
from celery import shared_task
from instaloader import Instaloader, Post, InstaloaderException
from googletrans import Translator
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pymorphy2
import re

from shared.models import Setting

from .models import InstagramPost, InstagramPostAnalysis

nltk.download('vader_lexicon')


@shared_task
def parse_instagram(location_id: str, to_date: str, max_count=20, likes_count=15, city_id=1) -> None:
    """

    Method parsing location post by giving location_id

    Метод позволяет парсить посты по данной локации

    :param location_id: Id of instagram location
    :param to_date: After the date parser stops its work
    :param max_count: Maximum of total parsed posts
    :param likes_count: Minimum likes count to filter post

    :return: List of location posts

    .. todo:: Add try for any errors that can happen while working
    """
    insta = Instaloader(download_comments=False, download_video_thumbnails=False,
                        download_videos=False, download_pictures=False)

    total_posts = set()

    count = 0

    try:
        for post in filter(_get_post_filter_function(to_date, likes_count),
                           insta.get_location_posts(location_id)):

            if count >= max_count:
                break

            total_posts.add(post)
            count += 1
    except InstaloaderException as e:
        print(e)  # todo add logging

    add_new_posts_to_db(total_posts)


def add_new_posts_to_db(posts: Iterable[Post]):
    """

    :param posts:
    :return:
    """
    for post in posts:
        try:
            post_db = InstagramPost(
                shortcode=post.shortcode,
                timestamp=post.date_utc,
                text=post.caption,
                likes=post.likes,
                comments_count=post.comments,
                post_lat=post.location.lat,
                post_lon=post.location.lng,
                owner=post.owner_username
            )
            post_db.save()
        except Exception as e:  # todo
            print(e)


@shared_task
def process_new_posts():
    """

    Processing new posts w/ sentiment analysis

    Обрабатывает необработанные посты, проверяя на рекламу и проводя сентиментальный анализ

    :return: None

    .. note:: Working w/ third-party api - google translator
    """

    unprocessed_posts = InstagramPost.objects.filter(processed=False)

    _is_post_not_advert_and_set_is_ad = partial(_is_post_not_advert, callback=_set_post_as_advert)
    clear_of_ads_posts = [post for post in filter(_is_post_not_advert_and_set_is_ad, unprocessed_posts)]

    sentiment_scores = _get_sentiment_score([post.text for post in clear_of_ads_posts])

    for post, score in zip(clear_of_ads_posts, sentiment_scores):
        result, created = InstagramPostAnalysis.objects.update_or_create(post=post, sentiment_score=score)
        result.save()

        post.processed = True
        post.save()


def _get_post_filter_function(to_date, likes_count):  # todo solve to_date problem
    return lambda post: post.caption is not None and post.likes > likes_count


def _is_post_not_advert(post, callback: Callable) -> bool:

    if not (is_post_ad_by_caption(post.caption) or is_post_ad_by_hashtag(post.caption_hashtags)):
        return True

    callback(post)
    return False


def _convert_text(text: str) -> str:
    """

    :param text: Raw text to text without
    :type text: str
    :return: Converted text
    ... todo:: Add text convertion
    """
    _hashtags_re = re.compile(r'(#.*)')
    _useless_characters_re = re.compile(r'[^\w\s\d,!?\'\"]')

    _text_without_hashtags = re.sub(_hashtags_re, '', text)
    _text_without_useless_stuff = re.sub(_useless_characters_re, '', _text_without_hashtags)
    return _text_without_useless_stuff


def _get_sentiment_score(texts: list) -> list:
    """

    :param texts:
    :type texts: str
    :return: from -1 to 1
    .. todo:: Add error handler
    """
    sentiment = SentimentIntensityAnalyzer()
    translator = Translator()
    results = []

    for text in texts:
        clear_text = _convert_text(text)

        try:
            translated_text = translator.translate(clear_text).text
        except Exception as e:
            print(e)  # todo
            translated_text = ' '

        sentiment_score = sentiment.polarity_scores(translated_text)
        results.append(sentiment_score['compound'])

    return results


def _set_post_as_advert(post: InstagramPost):
    post.is_ad = True
    post.processed = True
    post.save()


def _get_stop_words() -> list:
    return Setting.objects.get(name=settings.AD_FILTER_WORDS_DB_NAME).value.split(',')


def is_post_ad_by_caption(caption: str) -> bool:
    stop_words = _get_stop_words()

    morph = pymorphy2.MorphAnalyzer()
    caption = morph.parse(caption)[0].normal_form

    for word in stop_words:
        result = re.findall(morph.parse(word)[0].normal_form, str(caption))

        if result:
            return True

    return False


def is_post_ad_by_hashtag(hashtags: list) -> bool:
    stop_words = _get_stop_words()

    morph = pymorphy2.MorphAnalyzer()
    k = 0
    g = 0
    result = []

    while result == [] and k != len(stop_words):
        for i in stop_words:
            for j in range(len(hashtags)):

                hashtags[g] = morph.parse(hashtags[g])[0].normal_form
                result = re.findall(stop_words[k], str(hashtags[g]))
                g += 1

                if result:
                    return True

            if result:
                return True
            g = 0
            k += 1

    return False


@shared_task
def get_themes_from_time_to_time_from_city(from_time, to_time, city_id):

    pass


def _text_is_not_advert(text) -> bool:  # todo
    """

    Naive text advert checker. Works w/ list of stop-words

    :param text: Text to check if its advert
    :type text: str
    :return:

    .. note:: The function w/ reversed output (note the `not` in function name)
    """

    advert_words = (
        "надевать", "дизайн", "вопрос", "студия", "покупка", "предложение",
        "скидка", "новый", "этаж", "ссылка", "каблук",
        "заказ", "продавцы", "цена", "размер", "приобрести",
        "информация", "заказ", "наращивание", "запись", "заказать",
        "купить", "стоимость", "наличие", "примерка", "доставка", "адрес", "продажа", "инструкция")
    morph = pymorphy2.MorphAnalyzer()

    text_words = _convert_text(text).lower().split()
    for word in text_words:
        if morph.parse(word)[0].normal_form in advert_words:
            return False
    return True
