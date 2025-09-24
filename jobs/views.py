from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application

def index(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'jobs/index.html', {'jobs': jobs})

@login_required
def create(request):
    if not request.user.is_recruiter:
        return redirect('jobs.index')
    if request.method == 'POST':
        # Handle job creation form submission
        return redirect('jobs.index')
    return render(request, 'jobs/create.html')

@login_required
def applications(request):
    if request.user.is_recruiter:
        return redirect('recruiters.dashboard')
    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'jobs/applications.html', {'applications': applications})

def detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'jobs/detail.html', {'job': job})

@login_required
def edit(request, job_id):
    if not request.user.is_recruiter:
        return redirect('jobs.index')
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        # Handle job edit form submission
        return redirect('jobs.detail', job_id=job.id)
    return render(request, 'jobs/edit.html', {'job': job})

@login_required
def delete(request, job_id):
    if not request.user.is_recruiter:
        return redirect('jobs.index')
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        job.delete()
        return redirect('jobs.index')
    return render(request, 'jobs/delete.html', {'job': job})
