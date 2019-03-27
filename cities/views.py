from django.shortcuts import render, get_object_or_404

from .models import City


def get_cities(request):
    cities = City.objects.filter(active=True)
    return render(request, 'cities/all_cities.html', {'cities': cities})


def get_city_by_id(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    return render(request, 'cities/city_detail.html', {'city': city})
