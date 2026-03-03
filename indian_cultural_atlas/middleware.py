# indian_cultural_atlas/middleware.py

from django.http import Http404


# ==========================================
# Hide Admin From Non-Staff Users
# ==========================================
class HideAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated or not request.user.is_staff:
                raise Http404("Page not found")

        return self.get_response(request)


# ==========================================
# Disable Browser Cache (Fix Back Button)
# ==========================================
class DisableCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 🔥 Disable cache for ALL pages
        response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"

        return response