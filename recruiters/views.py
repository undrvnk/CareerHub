from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Applicant#, Application

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

        # ✅ Fetch all posts after saving
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'recruiters/index.html', {'posts': posts})
    
    # Show form page if GET request
    return render(request, 'recruiters/create.html')

# @login_required
# def applications(request):
#     if request.user.role == "recruiter":
#         return redirect('recruiters.dashboard')
#     applications = Application.objects.filter(applicant=request.user)
#     return render(request, 'jobs/applications.html', {'applications': applications})

def detail(request, job_id):
    post = get_object_or_404(Post, pk=job_id)
    return render(request, 'recruiters/detail.html', {'post': post})

@login_required
def edit(request, id):
    if not request.user.role == "recruiter":
        return redirect('recruiters.index')
    post = get_object_or_404(Post, pk=id)
    if request.method == 'GET':

        #post = Post.objects.get(id=id)
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
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'recruiters/index.html', {'posts': posts})
    return render(request, 'recruiters/edit.html', {'posts': post})

@login_required
def delete(request, id):
    if not request.user.role == "recruiter":
        return redirect('recruiters.index')
    post = get_object_or_404(Post, pk=id)
    
    post.delete()
    return redirect('recruiters.index')

@login_required
@login_required
def detail(request, id):
    # Get the job post
    post = get_object_or_404(Post, id=id)

    # Get all applicants for this post
    applicants = Applicant.objects.filter(post=post).order_by('-applied_at')

    # Separate applicants by stage
    applied_list = applicants.filter(stage='Applied')
    interview_list = applicants.filter(stage='Interview')
    offer_list = applicants.filter(stage='Offer')
    hired_list = applicants.filter(stage='Hired')

    # Pipeline stages and mapping
    stages = ['Applied', 'Interview', 'Offer', 'Hired']
    applicants_by_stage = {
        'Applied': applied_list,
        'Interview': interview_list,
        'Offer': offer_list,
        'Hired': hired_list,
    }

    # Render the detail page
    return render(request, 'recruiters/detail.html', {
        'post': post,
        'stages': stages,
        'applicants_by_stage': applicants_by_stage,
    })