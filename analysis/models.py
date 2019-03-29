from django.db import models

from instagram_parser.models import InstagramPost
from cities.models import City


class InstagramPostSentimentAnalysis(models.Model):
    post = models.ForeignKey(InstagramPost, models.CASCADE)
    sentiment_score = models.FloatField()

    def __str__(self):
        return "Пост %s" % self.post.shortcode

    class Meta:
        verbose_name = 'семантический анализ поста Instagram'
        verbose_name_plural = 'семантический анализ постов Instagram'


class InstagramPostsThemesByDate(models.Model):
    city = models.ForeignKey(City, models.SET_NULL, null=True, verbose_name='город')
    date_start = models.DateField(null=True, verbose_name='дата начала')
    date_end = models.DateField(null=True, verbose_name='дата конца')

    themes = models.TextField(verbose_name='темы')

    def __str__(self):
        return self.city.name + " " + str(self.date_start) + ' ' + str(self.date_end)

    class Meta:
        verbose_name = 'тематики постов'
        verbose_name_plural = verbose_name


__all__ = (
    'InstagramPostSentimentAnalysis',
    'InstagramPostsThemesByDate',
)
