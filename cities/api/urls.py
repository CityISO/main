from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import posts_with_scores_list, word_clouds_for_city

app_name = 'city-api'

urlpatterns = format_suffix_patterns([
    path('posts/<int:city_id>/', posts_with_scores_list, name='posts-w-scores-list'),
    path('words/<int:city_id>/', word_clouds_for_city, name='words-for-city')
], allowed=['json'])
