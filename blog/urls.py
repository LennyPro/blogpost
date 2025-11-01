from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('blog/', views.post_list, name='post_list'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:post>', views.get_post_details, name='get_post_details'),
    path('blog/comment/<int:post_id>/new', views.add_comment, name='add_comment'),
    path('blog/comment/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
    path('blog/comment/<int:comment_id>/edit', views.edit_comment, name='edit_comment'),
    path('blog/comment-form/<int:post_id>', views.comment_form, name='comment_form'),
    path('blog/<int:post_id>/share/', views.share_post, name='share_post'),
    path('blog/post/new', views.post_create_view, name='new_post'),
    path('blog/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('blog/<int:post_id>/update/', views.update_post, name='update_post'),
    path('blog/search', views.search_post, name='search_posts'),
    path('blog/post/top/', views.top_posts_view, name='top_posts'),
]
