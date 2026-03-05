# indian_cultural_atlas/middleware.py

from django.http import Http404


# ==========================================
# Hide Admin From Non-Staff Users
# ==========================================
# indian_cultural_atlas/middleware.py

from django.shortcuts import redirect
from django.http import Http404

# indian_cultural_atlas/middleware.py
from django.shortcuts import redirect
from django.http import Http404

# indian_cultural_atlas/middleware.py
from django.shortcuts import redirect

# indian_cultural_atlas/middleware.py
from django.shortcuts import redirect

class HideAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith('/admin/'):
            # Allow admin login/logout pages
            if path in ['/admin/login/', '/admin/logout/']:
                return self.get_response(request)

            user = getattr(request, 'user', None)

            # Only superusers can access other admin pages
            if not user or not user.is_authenticated or not user.is_superuser:
                # Normal users cannot see admin
                # Option 1: Redirect to home
                return redirect('home')
                # Option 2 (optional): Show 404 instead
                # raise Http404("Page not found")

        return self.get_response(request)
# ==========================================
# Disable Browser Cache (Fix Back Button)
# ==========================================
# ==========================================
# Disable Browser Cache (Fix Back Button)
# ==========================================

from django.shortcuts import redirect
from django.urls import reverse

class DisableCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # If user is not logged in and tries to access protected pages
        if not request.user.is_authenticated:
            protected_paths = [
                '/home/',
                '/profile/',
                '/settings/',
                '/update_profile/',
            ]

            if request.path in protected_paths:
                return redirect(reverse('login'))

        response = self.get_response(request)

        # Disable browser caching
        response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"

        return response