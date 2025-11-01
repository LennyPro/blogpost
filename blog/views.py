from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from blog.models import Post, Comment
from blog.forms import CommentForm, EmailForm, NewPostForm
from django.core.mail import send_mail
from unidecode import unidecode
from blog.forms import EditPostForm
from django.db.models import Q
from blog.utils import r, get_top_posts, update_post_views

from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, HttpResponse
from django.template.loader import render_to_string

# def post_list(request):
#     all_posts = Post.objects.all()
#     paginator = Paginator(all_posts, 3)
#     page_number = request.GET.get('page', 1)
#     posts = paginator.get_page(page_number)
#     return render(
#         request,
#         'blog/post/post_get_list.html',
#         {'posts': posts, 'all_posts': all_posts}
#     )


'''integrating partial reloading via HTMX using paginator --> '''


def post_list(request):
    all_posts = Post.objects.all()
    paginator = Paginator(all_posts, 2)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)

    if request.headers.get('HX-Request'):
        # return HttpResponse(render_to_string('endless_post_get_list.html',
        #                                      {'posts': posts})
        #                     )
        return HttpResponse(render_to_string('partial_post_get_list.html',
                                             {'posts': posts})
                            )

    return render(
        request,
        'blog/post/post_get_list.html',
        {'posts': posts})


#################################################################################
def get_post_details(request, year, month, day, post):
    post = get_object_or_404(Post, published__year=year, published__month=month, published__day=day, slug=post, )
    comments = post.comments.filter(active=True)

    try:
        # post_key = f'post:{post.id}:views'
        post_key = post.id
        # update_post_rating(post.id)
        update_post_views(post.id, 1)
        total_views = int(r.get(post_key))

    except (ConnectionError, TimeoutError):
        total_views = 0

    form = CommentForm()

    return render(
        request,
        'blog/post/post_get_details.html',
        {'post': post, 'comments': comments, 'form': form, 'total_views': total_views}
    )


@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(unidecode(post.title))
            post.save()
            return redirect('blog:post_list')
    else:
        form = NewPostForm()
    return render(request,
                  'blog/post/post_create.html',
                  {'form': form, })


def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    if request.method == "POST":
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:get_post_details',
                            year=post.published.year,
                            month=post.published.month,
                            day=post.published.day,
                            post=post.slug)
    else:
        form = EditPostForm(instance=post)
    return render(request, 'blog/post/post_update.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('accounts:profile_view')
    return render(request, 'blog/post/post_delete_confirm.html', {'post': post})


# ########################### MESSAGE BROKER ##########################################

@login_required()
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())  # create link of absolute type (https://...)
            # subject = f"{cd['sender']} recommends you check out {post.title}"
            subject = 'Hello World {}'.format(post.get_absolute_url().title())
            print('print:', subject)
            message = f"Check out the post '{post.title}' at the following link:\n{post_url}\n"
            send_mail(
                subject=subject,
                message=message,
                # from_email=[cd['email_from']],  # extract from User object !!!
                from_email='sender@test.com',
                recipient_list=[cd['email_to']],
            )
            sent = True
    else:  # which would be a GET request
        form = EmailForm()
    return render(
        request,
        'blog/post/post_share.html',
        {'post': post, 'form': form, 'sent': sent}
    )


# ############################# SEARCH ###########################################
def search_post(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)).order_by('-published')
    return render(request,
                  'blog/post/post_search_results.html',
                  {'results': results, 'query': query})


# ################################# REDIS as CACHE ########################################
def top_posts_view(request):
    top_posts = get_top_posts()
    return render(request, 'blog/post/post_top_10.html', {'top_posts': top_posts})


# ################################## COMMENT #########################################
# COMMENT

@login_required
def comment_form(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm()
    return render(request,
                  'blog/post/includes/comment_form.html',
                  {'post': post, 'form': form})


@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return render(
        request,
        'blog/post/comment_create_confirm.html',
        {'post': post, 'comment': comment, 'form': form}
    )


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect('blog:posts_list')
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(comment.post.get_absolute_url())
    else:
        form = CommentForm(instance=comment)
    return render(request,
                  'blog/post/comment_edit.html',
                  {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect('blog:post_list')
    if request.method == 'POST':
        comment.delete()
        return redirect(comment.post.get_absolute_url())
    return render(request,
                  'blog/post/comment_delete_confirm.html',
                  {'comment': comment})
