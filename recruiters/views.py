from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post#, Application
from profiles.models import Profile

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'recruiters/index.html', {'posts': posts})

@login_required
def create(request):
    if not request.user.role == "recruiter":
        return redirect('recruiters.index')
    if request.method == 'POST':
        # Handle job creation form submission
        post = Post()
        post.title = request.POST['title']
        post.company = request.POST['company']
        post.description = request.POST['description']
        post.location = request.POST['location']
        post.salary_range = request.POST['salary_range']
        post.recruiter = request.user
        post.save()
        return render(request, 'recruiters/create.html', {'posts': post})
    return render(request, 'recruiters/create.html')

# @login_required
# def applications(request):
#     if request.user.role == "recruiter":
#         return redirect('recruiters.dashboard')
#     applications = Application.objects.filter(applicant=request.user)
#     return render(request, 'jobs/applications.html', {'applications': applications})

@login_required
def candidates(request):
    name_term = request.GET.get('search_name')
    skill_term = request.GET.get('search_skill')
    education_term = request.GET.get('search_education')
    experience_term = request.GET.get('search_experience')
    if name_term or skill_term or education_term or experience_term:
        candidates = Profile.objects.filter(user__first_name__contains=name_term) | Profile.objects.filter(user__last_name__contains=name_term)
        candidates = candidates.filter(education__contains=education_term).filter(work_experience__contains=experience_term)
        if (skill_term):
            candidates = candidates.filter(skills__name__contains=skill_term)
    else:
        candidates = Profile.objects.all().order_by('-created_at')
    #candidates = Profile.objects.all().order_by('-created_at')
    return render(request, 'recruiters/candidates.html', {'candidates': candidates})

def detail(request, job_id):
    post = get_object_or_404(Post, pk=job_id)
    return render(request, 'posts/detail.html', {'post': post})

@login_required
def edit(request, id):
    if not request.user.role == "recruiter":
        return redirect('post.index')
    post = get_object_or_404(Post, pk=id)
    if request.method == 'GET':

        post = Post.objects.get(id=id)
        return render(request, 'recruiters/edit.html',

            {'posts': post})
    if request.method == 'POST':
        # Handle job edit form submission
        post = Post.objects.get(id=id)
        post.title = request.POST['title']
        post.company = request.POST['company']
        post.description = request.POST['description']
        post.location = request.POST['location']
        post.salary_range = request.POST['salary_range']
        post.recruiter = request.user
        post.save()
        return render(request, 'recruiters/create.html', {'posts': post})
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
