from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'location', ]


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=30,
                               min_length=3,
                               required=True,
                               label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username'}))

    first_name = forms.CharField(max_length=30,
                                 required=True,
                                 label='First Name',
                                 widget=forms.TextInput(attrs={'class': "form-control",
                                                               'placeholder': 'First Name'}))

    last_name = forms.CharField(max_length=30,
                                required=True,
                                label='Last Name',
                                widget=forms.TextInput(attrs={'class': "form-control",
                                                              'placeholder': 'Last name'}))

    email = forms.EmailField(max_length=100,
                             required=True,
                             label='Email',
                             widget=forms.EmailInput(attrs={'class': "form-control",
                                                            'placeholder': 'Email'}))

    password1 = forms.CharField(min_length=6,
                                max_length=100,
                                label='Password',
                                widget=forms.PasswordInput(attrs={'class': "form-control",
                                                                  'placeholder': 'Password'}))

    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'class': "form-control",
                                                                  'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
