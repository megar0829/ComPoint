from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm

cat_lst = ['취업고민', '직장인고민', '이직고민', '자유게시판']

@require_http_methods(['GET', 'POST'])
def index(request):
    categories = Category.objects.all()
    if not categories:
        for cat in cat_lst:
            category = Category()
            category.name = cat
            category.save()

    category1 = Category.objects.get(pk=1)
    category2 = Category.objects.get(pk=2)
    category3 = Category.objects.get(pk=3)
    category4 = Category.objects.get(pk=4)

    posts1 = category1.posts.all()[:5]
    posts2 = category2.posts.all()[:5]
    posts3 = category3.posts.all()[:5]
    posts4 = category4.posts.all()[:5]

    posts = Post.objects.all()

    context = {
        'category1': category1,
        'category2': category2,
        'category3': category3,
        'category4': category4,
        'posts1': posts1,
        'posts2': posts2,
        'posts3': posts3,
        'posts4': posts4,

        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def category_index(request, category_pk):
    category = Category.objects.get(pk=category_pk)
    posts = category.posts.all()

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'posts/category_index.html', context)


@require_http_methods(['GET', 'POST'])
def detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        post.delete()
        return redirect('posts:index')
    
    comment_form = CommentForm()
    comments = post.comment_set.all()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'posts/detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        category_name = request.POST.get('category')
        category = Category.objects.get(name=category_name)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.category = category
            form.save()
            return redirect('posts:detail', post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/create.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # if request.user == post.user:
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:detail', post.pk)
    else:
        form = PostForm(instance=post)
    # else:
    #     return redirect('posts:detail', post.pk)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'posts/update.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment_form.save()
            return redirect('posts:detail', post.pk)
    else:
        comment_form = CommentForm()
    comments = post.comment_set.all()
    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'posts/detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def comment_update(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('posts:detail', post_pk)
    
    post = get_object_or_404(Post, pk=post_pk)
    comments = Comment.object.all()    

    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts:detail.html', context)


@login_required
@require_http_methods(['POST'])
def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        return redirect('posts:detail', post_pk)


@login_required
@require_http_methods(['POST'])
def like(request, post_pk):
    post = Post.objects.get(pk=post_pk)

    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('posts:detail', post_pk)


@login_required
@require_http_methods(['POST'])
def comment_like(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    if request.user in comment.like_users.all():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('posts:detail', post_pk)


# def reply_create(request, post_pk, comment_pk):
#     post = get_object_or_404(Post, pk=post_pk)
#     comment = get_object_or_404(Comment, pk=comment_pk)
#     reply_form = ReplyForm(request.POST)
    
#     if reply_form.is_valid():
#         reply = reply_form.save(commit=False)
#         reply.comment = comment
#         reply.user = request.user
#         reply_form.save()
#         return redirect('posts:detail', post_pk)
    
#     replies = Reply.objects.all()
    
#     context = {
#         'post': post,
#         'comment': comment,
#         'reply_form': reply_form,
#         'replies': replies,
#     }
#     return render(request, 'posts/detail.html', context)


# def reply_detail(request, post_pk, comment_pk, reply_pk):
#     pass
