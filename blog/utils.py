import redis
from django.conf import settings
from blog.models import Post

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, )


def update_post_views(post_id, increment_by=1):
    view_key = post_id  # Redis key for storing view count
    return r.incrby(view_key, increment_by)


def update_post_rating(post_id):
    view_key = post_id  # Redis key for storing view count
    rating_key = 'posts:rating'  # Redis key for storing ratings
    current_view = int(r.get(view_key) or 0)  # Get the current view count
    r.zadd(rating_key, {post_id: current_view})


def get_top_posts(limit=10):
    posts_with_scores = r.zrevrange('posts:rating', 0, limit - 1, withscores=True)
    post_ids = [int(post_id) for post_id, _ in posts_with_scores]
    posts = Post.objects.filter(id__in=post_ids)
    result = []
    for post in posts:
        score = next((score for post_id, score in posts_with_scores if int(post_id) == post.id), None)
        result.append((post, int(score)))
    return result
