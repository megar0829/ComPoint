from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, MyAuthenticationForm, CustomPasswordChangeForm
from django.contrib.auth import get_user_model

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('info:index')
    
    if request.method == 'POST':
        form = MyAuthenticationForm(request, request.POST)
        if form.is_valid():
            # 로그인 세션 생성
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'info:index')
    else :
        form = MyAuthenticationForm()
    context = {
        'form':form, 
    }
    return render(request,'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('info:index')


def signup(request):
    # 로그인한 사용자가 계정생성하는 것 막기
    if request.user.is_authenticated :
        return redirect('info:index')
    # 계정생성
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('info:index')
    else :
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def delete(request):
    request.user.delete() # 로그인한 유저 계정 삭제
    return redirect('info:index')    


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        # pw_form = CustomPasswordChangeForm(request.user, request.POST)
        # if form.is_valid() and pw_form.is_valid():
        if form.is_valid():
            form.save()
            # pw_form.save()
            return redirect('accounts:profile', request.user.username)
    else :
        form = CustomUserChangeForm(instance=request.user)
        # pw_form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
        # 'pw_form': pw_form,
    }
    return render(request, 'accounts/update.html', context)

@login_required
def change_password(request, username):
    if request.method =='POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user= form.save()
            update_session_auth_hash(request, user)
            return redirect('info:index')
    else :
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form':form,
    }
    return render(request, 'accounts/change_password.html', context)



def profile(request, username):
    # 유저 정보
    user = get_user_model().objects.get(username=username)
    posts = user.post_set.all()
    comments = user.comment_set.all()
    gongos = user.bookmark_gongos.all()
    context = {
        'user':user,
        'posts':posts,
        'comments':comments,
        'gongos':gongos,
    }
    return render(request, 'accounts/profile.html', context)