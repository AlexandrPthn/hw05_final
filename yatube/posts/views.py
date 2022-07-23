from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


def get_paginator(queryset, request):
    paginator = Paginator(queryset, settings.PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    page = get_paginator(
        Post.objects.select_related(
            'author', 'group'), request)
    return render(request, 'posts/index.html', {'page_obj': page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    page = get_paginator(
        group.posts.select_related('author', 'group'),
        request)
    context = {
        'group': group,
        'page_obj': page,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related('author', 'group')
    page = get_paginator(post_list, request)
    following = request.user.is_authenticated and author.following.filter(
        user=request.user).exists()
    context = {
        'author': author,
        'post_count': page.paginator.count,
        'page_obj': page,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related(
            'author', 'group'), pk=post_id)
    comments = post.comments.all()
    posts_count = post.author.posts.count()
    context = {
        'comments': comments,
        'post_count': posts_count,
        'post': post,
        'form': CommentForm(),
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_id = request.user.id
            post.save()
            return redirect('posts:profile', request.user.username)
        return render(request, template, {'form': form})
    form = PostForm()
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    page = get_paginator(
        Post.objects.filter(
            author__following__user=request.user),
        request)
    return render(request, 'posts/follow.html', {'page_obj': page})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    profile_follow = get_object_or_404(Follow,
                                       author=author,
                                       user=request.user)
    profile_follow.delete()
    return redirect('posts:profile', username=username)
