from django.contrib import admin
from blog.models import Post, Comment
from tinymce.widgets import TinyMCE  # text editor for "new line" insertions
from django.db import models


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published', 'status']
    prepopulated_fields = {'slug': ('title',)}  # take slug from title
    ordering = ['status', 'published']
    list_filter = ['status']
    formfield_overrides = {models.TextField: {'widget': TinyMCE}}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email']
