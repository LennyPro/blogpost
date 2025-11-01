from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from accounts.forms import EditProfileForm, CustomUserCreationForm

from accounts.models import Profile
from blog.models import Post

from python_telegram_auth import verify_auth_data
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User


def register_view(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('accounts:profile_view')
    else:
        # form = UserCreationForm()
        form = CustomUserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:profile_view')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login_view')


@login_required
def profile_view(request):
    profile = Profile.objects.filter(user=request.user)
    profile_posts = Post.objects.filter(author=request.user)
    return render(request,
                  'registration/profile.html',
                  {"profile_posts": profile_posts, "profile": profile})


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile_view')
    else:
        form = EditProfileForm(instance=request.user.profile)
    return render(request, 'registration/profile_edit.html', {"form": form})


def telegram_login_complete(request):
    data = request.GET.dict()

    try:
        user_data = verify_auth_data(data=data, bot_token=settings.TELEGRAM_BOT_TOKEN)
    except ValueError:
        return HttpResponseBadRequest('Invalid Telegram Token')

    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={'first_name': user_data.get('first_name', ''), }
    )

    if created:
        user.set_unusable_password()
        user.save()

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return redirect('accounts:profile_view')

# ################### Version 2 #######################################################

# import hashlib
# import hmac

# def verify_telegram_auth(data: dict, token: str) -> bool:
#     auth_data = data.copy()
#     hash_received = auth_data.pop('hash')
#     secret_key = hashlib.sha256(token.encode()).digest()
#     check_string = '\n'.join([f"{k}={v}" for k, v in sorted(auth_data.items())])
#     hmac_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
#     return hmac_hash == hash_received
#
#
# def telegram_login_complete(request):
#     data = request.GET.dict()
#
#     if not verify_telegram_auth(data=data, token=settings.TELEGRAM_TOKEN):
#         return HttpResponseBadRequest('Invalid Telegram login')
#
#     user_data = data.get('username')
#
#     user, created = User.objects.get_or_create(
#         username=user_data,
#         defaults={'first_name': data.get('first_name', ''), }
#     )
#
#     if created:
#         user.set_unusable_password()
#         user.save()
#
#     user.backend = 'django.contrib.auth.backends.ModelBackend'
#     login(request, user)
#     return redirect('accounts:profile_view')

# ###########################################################################
