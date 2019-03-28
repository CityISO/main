from django.contrib import admin

from .models import InstagramPostSentimentAnalysis


@admin.register(InstagramPostSentimentAnalysis)
class InstagramPostAnalysisAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cut_text', 'sentiment_score')

    def cut_text(self, obj):
        return obj.post.text[:100]

    cut_text.short_description = 'вырезка из текста'

