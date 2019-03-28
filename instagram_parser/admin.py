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
