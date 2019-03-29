from django.urls import path, include

from .views import get_cities, get_city_by_id

app_name = 'cities'

urlpatterns = [
    path('', get_cities, name='index'),
    path('<int:city_id>/', get_city_by_id, name='get-city-by-id'),
    path('api/', include('cities.api.urls', namespace='city-api')),
]