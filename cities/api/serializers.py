from rest_framework import serializers

from analysis.models import InstagramPostsThemesByDate

class PostWithAvgScoreSerializer(serializers.Serializer):
    date = serializers.DateField()
    avg_score = serializers.FloatField()


class WordCloudSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstagramPostsThemesByDate
        fields = ['date_start', 'date_end', 'themes']
