import requests
from django.utils import timezone

from foodcartapp.models import PlaceCoordinate
from star_burger.settings import COORDS_CACHE_EXPIRES_SEC, GEO_CODER_KEY


def get_coodinates(address):
    place, created = PlaceCoordinate.objects.get_or_create(address=address)
    if created or (timezone.now() -
                   place.date).seconds >= COORDS_CACHE_EXPIRES_SEC:
        place.lat, place.lon = fetch_coordinates_from_yandex_api(address)
        place.save()
    return tuple([place.lat, place.lon])


def fetch_coordinates_from_yandex_api(address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": address, "apikey": GEO_CODER_KEY, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    found_places = \
        response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return tuple([lat, lon])
