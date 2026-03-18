# myproject/middleware.py

import time
import logfire
from django.urls import resolve, Resolver404

class PageLoadTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define a histogram metric for page load times.
        # Histograms are great for durations as they provide distribution insights.
        # 'unit' helps Logfire understand the measurement (miliseconds in this case).
        self.page_load_histogram = logfire.metric_histogram(
            'django_page_load_time',
            unit='ms', #miliseconds
            description='Time taken to load a single Django page (server-side) in ms.'
        )

    def __call__(self, request):
        # Record the start time when the request enters the middleware.
        start_time = time.monotonic()

        # Process the request and get the response.
        response = self.get_response(request)

        # Calculate the duration after the response has been generated.
        duration = time.monotonic() - start_time

        # Get the view name or URL path for better metric categorization.
        view_name = "unknown_view"
        try:
            match = resolve(request.path_info)
            if match.view_name:
                view_name = match.view_name
            elif hasattr(match.func, '__name__'):
                view_name = match.func.__name__
            elif hasattr(match.func, '__class__'):
                view_name = match.func.__class__.__name__
        except Resolver404:
            # If URL doesn't resolve, use the path directly
            view_name = request.path

        # Record the duration using the histogram metric.
        # We add 'path' and 'view_name' as attributes to allow filtering and analysis
        # by specific pages in the Logfire dashboard.
        self.page_load_histogram.record(
            duration,
            attributes={
                'http.method': request.method,
                'http.target': request.path,
                'django.view_name': view_name,
                'http.status_code': response.status_code,
            }
        )

        return response
