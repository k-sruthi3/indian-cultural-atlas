from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

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

class CustomLoginView(LoginView):
    template_name = 'culture/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


# =========================
# LOGOUT
# =========================

@never_cache
def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('sessionid')
    return response


# =========================
# HOME
# =========================

@never_cache
@login_required
def home(request):
    states = State.objects.all().order_by('name')
    return render(request, 'culture/index.html', {'states': states})


# =========================
# PROFILE
# =========================

@never_cache
@login_required
def profile_view(request):
    return render(request, 'culture/profile.html')


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

    state = State.objects.filter(name__icontains=query).first()
    if state:
        return redirect("state_detail", state_id=state.id)

    district = District.objects.filter(name__icontains=query).first()
    if district:
        return redirect("district_detail", district_id=district.id)

    return render(request, "culture/not_found.html", {"query": query})


# =========================
# CONTACT
# =========================

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

def help_view(request):
    return render(request, 'culture/help.html')


# =========================
# CUSTOM 404
# =========================

def custom_404(request, exception):
    return render(request, 'culture/404.html', status=404)