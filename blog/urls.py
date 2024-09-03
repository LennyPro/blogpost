from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.get_post_details, name='get_post_details'),
    path('<int:post_id>/comment', views.add_comment, name='add_comment'),
    path('<int:post_id>/share/', views.share_post, name='share_post'),
]
