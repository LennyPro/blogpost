from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        BANNED = 'BN', 'Banned'
        DELETED = 'DL', 'Deleted'

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    poem_by = models.CharField(max_length=50, default='Unknown')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=200, unique=True, unique_for_date="published")
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:get_post_details',
            args=[self.published.year,self.published.month,self.published.day, self.slug]
        )

    class Meta:
        ordering = ['-published']
        # verbose_name = 'Объявление'
        # verbose_name_plural = 'Объявления'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=120)
    email = models.EmailField()
    body = models.TextField(verbose_name='comment area')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Written by: {self.name} about: {self.post}'


