from django.contrib import admin
from django.utils.html import format_html

from .models import InstagramPost, InstagramPostAnalysis


@admin.register(InstagramPost)
class InstagramPostAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('__str__', 'processed', 'custom_instagram_link', 'is_ad')

    def custom_instagram_link(self, obj):
        return format_html(
            '<a href="https://instagram.com/p/{}" target="_blank">{}</a>',
            obj.shortcode,
            obj.shortcode
        )

    custom_instagram_link.short_description = 'ссылка на пост'


@admin.register(InstagramPostAnalysis)
class InstagramPostAnalysisAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cut_text', 'sentiment_score')

    def cut_text(self, obj):
        return obj.post.text[:100]

    cut_text.short_description = 'вырезка из текста'
