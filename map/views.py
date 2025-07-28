from django.http import HttpResponse
from .models import Location
import folium


def map_page(request):
    center = (31.7771, -40.24965)
    folium_map = folium.Map(location=center, zoom_start=2)
    return HttpResponse(folium_map.get_root().render())
