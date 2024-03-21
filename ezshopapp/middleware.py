# myapp/middleware.py

from django.utils.cache import add_never_cache_headers

class DisableClientSideCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Apply cache control headers to every response
        add_never_cache_headers(response)
        return response
