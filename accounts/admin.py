from django.contrib import admin
from accounts.models import Profile
from django.db import models


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date', 'bio', 'location']