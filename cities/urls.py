from django.urls import path

from .views import get_cities, get_city_by_id

app_name = 'cities'

urlpatterns = [
    path('', get_cities, name='index'),
    path('<int:city_id>/', get_city_by_id, name='get-city-by-id'),
]