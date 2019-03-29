from django.shortcuts import render, get_object_or_404

from .models import City, CityPeoplePhoto


def get_cities(request):
    cities = City.objects.filter(active=True)
    return render(request, 'cities/all_cities.html', {'cities': cities})


def get_city_by_id(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    photos = CityPeoplePhoto.objects.filter(city_id=city_id)
    return render(request, 'cities/city_detail.html', {'city': city, 'citizen_photos': photos})
