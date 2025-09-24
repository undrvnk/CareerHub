from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post#, Application

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'recruiters/index.html', {'posts': posts})

@login_required
def create(request):
    if not request.user.role == "recruiter":
        return redirect('recruiters.index')
    if request.method == 'POST':
        # Handle job creation form submission
        return redirect('recruiters.index')
    return render(request, 'recruiters/create.html')

# @login_required
# def applications(request):
#     if request.user.role == "recruiter":
#         return redirect('recruiters.dashboard')
#     applications = Application.objects.filter(applicant=request.user)
#     return render(request, 'jobs/applications.html', {'applications': applications})

def detail(request, job_id):
    post = get_object_or_404(Post, pk=job_id)
    return render(request, 'posts/detail.html', {'post': post})

@login_required
def edit(request, post_id):
    if not request.user.role == "recruiter":
        return redirect('post.index')
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        # Handle job edit form submission
        return redirect('posts.detail', post_id=post.id)
    return render(request, 'posts/edit.html', {'post': post})

@login_required
def delete(request, post_id):
    if not request.user.role == "recruiter":
        return redirect('post.index')
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('posts.index')
    return render(request, 'posts/delete.html', {'post': post})
