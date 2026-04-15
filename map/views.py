import logfire
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from blog.models import Post
from .models import Location
import folium


def map_page(request):
    center = (31.7771, -40.24965)

    with logfire.span('map page'):
        with logfire.span('fetch locations'):
            locations = list(Location.objects.all())

        with logfire.span('build folium map', location_count=len(locations)):
            folium_map = folium.Map(location=center, zoom_start=2)
            for location in locations:
                popup = f'<a href="/map/{location.name}">{location.name}</a>'
                folium.Marker(
                    location=[location.latitude, location.longitude],
                    popup=popup,
                ).add_to(folium_map)

        with logfire.span('render map html'):
            map_html = folium_map.get_root().render()

    return HttpResponse(map_html)


def post_list_by_location(request, name):
    with logfire.span('posts by location', location=name):
        with logfire.span('fetch location', name=name):
            location = Location.objects.get(name__iexact=name)

        with logfire.span('build location map'):
            folium_map = folium.Map(
                location=[location.latitude, location.longitude],
                zoom_start=4, width=400, height=300,
            )
            folium.Marker(
                location=[location.latitude, location.longitude],
                popup=location.name,
            ).add_to(folium_map)
            location_map = folium_map._repr_html_()

        with logfire.span('fetch posts for location'):
            posts = list(Post.objects.filter(
                location=location,
                published_date__lte=timezone.now(),
            ).order_by('-published_date'))

    return render(request, 'map/post_list_by_location.html', {
        'posts': posts,
        'location': location,
        'location_map': location_map,
    })
