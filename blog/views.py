from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from blog.models import Post
from django.views.decorators.http import require_POST
from blog.forms import CommentForm, EmailForm
from django.core.mail import send_mail


def post_list(request):
    all_posts = Post.objects.all()
    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def get_post_details(request, year, month, day, post):
    post_details = get_object_or_404(Post, published__year=year, published__month=month, published__day=day, slug=post,)
    comments = post_details.comments.filter(active=True)
    form = CommentForm()
    return render(
        request,
        'blog/post/post.html',
        {'post': post_details, 'comments': comments, 'form': form}
    )


# this method is for both GET and POST requests
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())  # create link of absolute type (https://...)
            # subject = f"{cd['name']} recommends you check out {post.title}"
            subject = f"{cd['name']} recommends you {post.title}".replace('\n', '').replace('\r', '')
            message = f"Check out the post '{post.title}' at the following link:\n{post_url}\n"
            send_mail(
                subject=subject,
                message=message,
                from_email="sender@email.com",
                recipient_list=[cd['email_to']]
            )
            sent = True
    else:  # which would be a GET request
        form = EmailForm()
    return render(
        request,
        'blog/post/share_post.html',
        {'post': post, 'form': form, 'sent': sent}
    )


def update_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.title = 'updates title'
    post.save()
    return render(
        request,
        'blog/post/post.html',
        {'post': post}
    )


def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()


@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {'post': post, 'comment': comment, 'form': form}
    )
