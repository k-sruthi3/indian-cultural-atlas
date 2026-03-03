# culture/urls.py
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView


urlpatterns = [

    # Root → Redirect based on login
    path('', views.root_redirect, name='root'),

    # =============================
    # Authentication
    # =============================
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # =============================
    # Home
    # =============================
    path('home/', views.home, name='home'),

    # =============================
    # Profile & Settings
    # =============================
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('delete-account/', views.delete_account, name='delete_account'),

    # =============================
    # Password Change
    # =============================
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='culture/change_password.html',
            success_url=reverse_lazy('culture:password_change_done')
        ),
        name='change_password'
    ),

    path(
        'change-password/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='culture/change_password_done.html'
        ),
        name='password_change_done'
    ),

    # =============================
    # State & District
    # =============================
    path(
        'state/<int:state_id>/',
        views.state_detail,
        name='state_detail'
    ),

    path(
        'district/<int:district_id>/',
        views.district_detail,
        name='district_detail'
    ),

    # =============================
    # Other Features
    # =============================
    path('search/', views.search_view, name='search'),
    path('help/', views.help_view, name='help'),
    path('contact/', views.contact_support, name='contact_support'),
]