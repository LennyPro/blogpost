from accounts import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit', views.profile_edit_view, name='profile_edit_view'),
    path('login/telegram/complete/', views.telegram_login_complete, name='telegram_login_complete'),
]
