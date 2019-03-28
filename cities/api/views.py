from rest_framework import views
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.db.models.functions import TruncDate
from django.db.models import Avg

from analysis.models import InstagramPostSentimentAnalysis, InstagramPostsThemesByDate
from .serializers import PostWithAvgScoreSerializer, WordCloudSerializer


@api_view(['GET'])
@cache_page(60 * 60 * 2)
def posts_with_scores_list(request, city_id: int):
    data = InstagramPostSentimentAnalysis.objects\
        .filter(post__city_id=city_id).annotate(date=TruncDate('post__timestamp'))\
        .values('date').annotate(avg_score=Avg('sentiment_score')).values('date', 'avg_score')

    return Response([PostWithAvgScoreSerializer(entity).data for entity in data])


@api_view(['GET'])
@cache_page(60 * 60 * 10)
def word_clouds_for_city(request, city_id):
    themes = InstagramPostsThemesByDate.objects.filter(city_id=city_id)[0]
    return Response(WordCloudSerializer(themes).data)
