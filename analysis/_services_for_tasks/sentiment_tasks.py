from typing import Callable

import re
from functools import partial


from django.conf import settings
import pymorphy2
import emoji
import indicoio

from shared.models import Setting
from instagram_parser.models import InstagramPost

from analysis.models import InstagramPostSentimentAnalysis

indicoio.config.api_key = settings.INDICOIO_API_KEY

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
        result, created = InstagramPostSentimentAnalysis.objects.update_or_create(post=post, sentiment_score=score)
        result.save()

        post.processed = True
        post.save()


def _is_post_not_advert(post, callback: Callable) -> bool:

    if not is_post_ad_by_caption(post.text):
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
    _text_without_emoji = _get_emoji_free_text(_text_without_hashtags)
    _text_without_useless_stuff = re.sub(_useless_characters_re, '', _text_without_emoji)
    return _text_without_useless_stuff


def _get_sentiment_score(texts: list) -> list:
    """

    :param texts:
    :type texts: list
    :return: from -1 to 1
    .. todo:: Add error handler
    """
    results = []

    for chunk in chunks(texts, 90):
        res = indicoio.sentiment(chunk, language='ru')
        results.extend(res)

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


def _get_emoji_free_text(text):
    return re.sub(emoji.get_emoji_regexp(), ' ', text)


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


__all__ = (
    'process_new_posts',
)
