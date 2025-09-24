from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def login(request):
    if request.user.is_authenticated:
        return redirect('jobs.index')
    if request.method == 'POST':
        # Handle login form submission
        return redirect('jobs.index')
    return render(request, 'accounts/login.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('jobs.index')
    if request.method == 'POST':
        # Handle signup form submission
        return redirect('jobs.index')
    return render(request, 'accounts/signup.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('jobs.index')
