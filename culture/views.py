from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from .models import State
from django.db.models import Q

from .models import State, Festival, DanceForm, District, Profile
from .forms import ProfileUpdateForm, ContactForm


# =========================
# ROOT REDIRECT
# =========================

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')


# =========================
# CUSTOM LOGIN VIEW
# =========================

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

@method_decorator(never_cache, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'culture/login.html'
    authentication_form = AuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f"Welcome {form.get_user().username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password!")
        return super().form_invalid(form)
# =========================
# LOGOUT
# =========================

@never_cache
def logout_view(request):
    logout(request)
    request.session.flush()   # completely destroy session
    return redirect('login')

# =========================
# HOME
# =========================

@never_cache
@login_required


def home(request):
    states = State.objects.all()[:6]  # Only show first 6 states
    return render(request, 'culture/index.html', {'states': states})

# =========================
# PROFILE
# =========================



@never_cache
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'culture/profile.html', {
        'profile': profile
    })


@never_cache
@login_required
def settings_view(request):
    return render(request, 'culture/settings.html')


# =========================
# UPDATE PROFILE
# =========================

@never_cache
@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        email = request.POST.get("email")
        request.user.email = email
        request.user.save()

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'culture/update_profile.html', {'form': form})


# =========================
# DELETE ACCOUNT
# =========================

@never_cache
@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect('login')

    return render(request, 'culture/delete_account.html')


# =========================
# REGISTER
# =========================
@never_cache

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'culture/register.html')


# =========================
# STATE DETAIL
# =========================

@never_cache
@login_required
def state_detail(request, state_id):
    state = get_object_or_404(State, id=state_id)
    festivals = Festival.objects.filter(state=state)
    dances = DanceForm.objects.filter(state=state)
    districts = District.objects.filter(state=state)

    return render(request, 'culture/state_detail.html', {
        'state': state,
        'festivals': festivals,
        'dances': dances,
        'districts': districts
    })


# =========================
# DISTRICT DETAIL
# =========================

@never_cache
@login_required
def district_detail(request, district_id):
    district = get_object_or_404(District, id=district_id)
    return render(request, 'culture/district_detail.html', {'district': district})


# =========================
# SEARCH
# =========================



@never_cache
@login_required
def search_view(request):
    query = request.GET.get("q", "").strip()
    
    if not query:
        return render(request, "culture/not_found.html", {"query": query})

    # Search States
    state = State.objects.filter(
        Q(name__icontains=query) |
        Q(famous_food__icontains=query) |
        Q(famous_dance__icontains=query) |
        Q(famous_folk_art__icontains=query) |
        Q(famous_temple__icontains=query) |
        Q(traditional_dress__icontains=query) |
        Q(monuments__icontains=query)
    ).first()
    if state:
        return redirect("state_detail", state_id=state.id)

    # Search Districts
    district = District.objects.filter(
        Q(name__icontains=query) |
        Q(famous_food__icontains=query) |
        Q(famous_festival__icontains=query) |
        Q(famous_temple__icontains=query) |
        Q(famous_monument__icontains=query)
    ).first()
    if district:
        return redirect("district_detail", district_id=district.id)

    # Search Festivals
    festival = Festival.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ).first()
    if festival:
        return redirect("state_detail", state_id=festival.state.id)

    # Search DanceForms
    dance = DanceForm.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ).first()
    if dance:
        return redirect("state_detail", state_id=dance.state.id)

    # If nothing found
    return render(request, "culture/not_found.html", {"query": query})
# =========================
# CONTACT
# =========================

@never_cache
@login_required
def contact_support(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['message'],
                settings.DEFAULT_FROM_EMAIL,
                ['your_email@gmail.com'],
            )
            return render(request, 'culture/contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'culture/contact.html', {'form': form})


# =========================
# HELP
# =========================

@never_cache
@login_required
def help_view(request):
    return render(request, 'culture/help.html')

# =========================
# CUSTOM 404
# =========================

def custom_404(request, exception):
    return render(request, 'culture/404.html', status=404)


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# -----------------------------
# Password Change View
# -----------------------------
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

# ------------------------------
# Change Password View
# ------------------------------
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

# ------------------------------
# Change Password View
# ------------------------------
@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in for the current session
            update_session_auth_hash(request, user)
            # Set a session flag to allow success page
            request.session['password_changed'] = True
            return redirect('password_change_done')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'culture/change_password.html', {'form': form})


# ------------------------------
# Password Change Done View
# ------------------------------
@login_required
def password_change_done_view(request):
    if request.session.get('password_changed'):
        # Remove the session flag so success page can’t be re-used
        del request.session['password_changed']
        return render(request, 'culture/change_password_done.html')
    else:
        # User tried to access success page directly or hit back → log out
        logout(request)
        return redirect('login')