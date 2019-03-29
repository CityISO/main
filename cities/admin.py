from django.contrib import admin

from instagram_parser.models import InstagramPost

from .models import City, CityPeoplePhoto


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'posts_count', 'active')

    def posts_count(self, obj):
        return InstagramPost.objects.filter(city=obj).count()

    posts_count.short_description = 'кол-во постов'


admin.site.register(CityPeoplePhoto)
