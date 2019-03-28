from typing import Iterable

from celery import shared_task
from instaloader import Instaloader, Post, InstaloaderException
import nltk

from .models import InstagramPost

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
    :param city_id:

    :return: List of location posts

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

    add_new_posts_to_db(total_posts, city_id=city_id)


def _get_post_filter_function(to_date, likes_count):  # todo solve to_date problem
    return lambda post: post.caption is not None and post.likes > likes_count


def add_new_posts_to_db(posts: Iterable[Post], city_id=1):
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
                owner=post.owner_username,
                city_id=city_id
            )
            post_db.save()
        except Exception as e:  # todo
            print(e)
