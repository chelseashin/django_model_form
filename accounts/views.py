from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash, get_user_model
from .forms import UserCustomChangeForm, UserCustomCreationForm


# Create your views here.
# 회원가입
def signup(request):
    # 회원가입 create 동작
    if request.user.is_authenticated:    # 로그인 되어있는지 상태 확인 - 로그인 되어있으면
        return redirect('boards:index')
        
    if request.method == "POST":
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save()           # 1
            auth_login(request, user)    # 2
            return redirect('boards:index')
    # 페이지 띄워주기
    else:
        form = UserCustomCreationForm()
    context = {'form': form}
    return render(request, 'accounts/auth_form.html', context)
    
# 로그인
def login(request):
    if request.user.is_authenticated:     # 로그인 한 사람이 로그인하려하면
        return redirect('boards:index')
        
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.POST.get('next') or 'boards:index')
    else:
        form = AuthenticationForm()
    context = {'form': form,
               'next': request.GET.get('next', ''),    # next가 아니면 빈 칸을 넣어줌
    }
    return render(request, 'accounts/login.html', context)
    
# 로그아웃
def logout(request):
    auth_logout(request)
    return redirect('boards:index')
    
# 회원탈퇴
def delete(request):
    user = request.user          # 변수에 담아서 삭제
    if request.method == 'POST':
        # DELETE
        user.delete()
        
    return redirect('boards:index')
    
# 회원정보수정
def edit(request):
    if request.method == 'POST':
        form = UserCustomChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('boards:index')
    else:
        form = UserCustomChangeForm(instance=request.user)
    context = {'form': form,}
    return render(request, 'accounts/auth_form.html', context)
    
def change_password(request):
    if request.method == "POST":
        # 인자 순서 유의. 인스턴스 없음
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)    # 현재 유저가 로그아웃 되는 것을 막는다.
            return redirect('boards:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form,}
    return render(request, 'accounts/auth_form.html', context)
    
def profile(request, user_pk):
    user_info = get_object_or_404(get_user_model(), pk=user_pk)
    context = {
        'user_info': user_info,
    }
    return render(request, "accounts/profile.html", context)