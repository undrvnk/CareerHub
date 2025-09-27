from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from recruiters.models import Post

def index(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'jobs/index.html', {'jobs': jobs})

@login_required
def create(request):
    if not request.user.role == "recruiter":
        return redirect('jobs.index')
    if request.method == 'POST':
        # Handle job creation form submission
        return redirect('jobs.index')
    return render(request, 'jobs/create.html')

@login_required
def applications(request):
    if request.user.role == "recruiter":
        return redirect('jobs.index')
    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'jobs/applications.html', {'applications': applications})

def detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'jobs/detail.html', {'job': job})

@login_required
def edit(request, job_id):
    if not request.user.role == "recruiter":
        return redirect('jobs.index')
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        # Handle job edit form submission
        return redirect('jobs.detail', job_id=job.id)
    return render(request, 'jobs/edit.html', {'job': job})

@login_required
def delete(request, job_id):
    if not request.user.role == "recruiter":
        return redirect('jobs.index')
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        job.delete()
        return redirect('jobs.index')
    return render(request, 'jobs/delete.html', {'job': job})

@login_required
def view_applications(request, post_id):
    if request.user.role == "recruiter":
        return redirect('jobs.index')
    job = get_object_or_404(Post, pk=post_id)
    applications = Application.objects.filter(job=job)
    return render(request, 'jobs/view_applications.html', {'job': job, 'applications': applications})

@login_required
def apply(request, post_id):
    if request.user.role == "recruiter":
        return redirect('accounts.login')
    job = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        # Handle job application form submission
        application = Application()
        application.post = Post
        application.applicant = request.user
        application.status = 'applied'
        application.note = request.POST['note']
        application.updated_at = request.POST['updated_at']
        application.created_at = request.POST['created_at']
        #application.cover_letter = request.POST['cover_letter']
        #application.resume = request.FILES.get('resume')
        application.save()
        return redirect('jobs.detail', job_id=job.id)
    return render(request, 'jobs/apply.html', {'job': job})