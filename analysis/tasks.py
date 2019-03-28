from celery import shared_task

from ._services_for_tasks.sentiment_tasks import process_new_posts as _process_new_posts
from ._services_for_tasks.thematic_modeling_tasks import generate_save_themes_by_city_from_date_to_date \
    as _generate_save_themes_by_city_from_date_to_date


@shared_task
def process_new_posts():
    return _process_new_posts()


@shared_task
def generate_themes_by_city_from_date_to_date(city_id:int, from_date:str, to_date:str):
    return _generate_save_themes_by_city_from_date_to_date(city_id, from_date, to_date)


