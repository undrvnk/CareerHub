# jobs/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application               
from recruiters.models import Post as JobPost
from .forms import ApplicationForm


def index(request):
    jobs = JobPost.objects.all().order_by('-created_at') 
    return render(request, 'jobs/index.html', {'jobs': jobs})


@login_required 
def detail(request, job_id):
    job = get_object_or_404(JobPost, pk=job_id) 
    
    # Check if the user has already applied
    has_applied = Application.objects.filter(job_id=job.id, applicant=request.user).exists()
    is_recruiter = request.user.role == 'recruiter'

    if request.method == 'POST':
        if is_recruiter or has_applied:
            messages.error(request, "Cannot apply for this job.")
            return redirect('jobs.detail', job_id=job.id)

        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = Application(
                job=job, 
                applicant=request.user,
                note=form.cleaned_data['note']
            )
            application.save()
            messages.success(request, f"Successfully applied for {job.title} at {job.company}!")
            return redirect('jobs.applications')
    else:
        form = ApplicationForm()
    
    return render(request, 'jobs/detail.html', {
        'job': job,
        'form': form,
        'has_applied': has_applied,
        'is_recruiter': is_recruiter,
    })


@login_required
def applications(request):
    # Job Seeker View: Show applications they have submitted
    if request.user.role == "recruiter":
        return redirect('recruiters.index') 
        
    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'jobs/applications.html', {'applications': applications})

@login_required
def create(request):
    if not request.user.role == "recruiter":
        return redirect('jobs.index')
    return redirect('recruiters.create')

@login_required
def edit(request, job_id):
    if not request.user.role == "recruiter":
        return redirect('jobs.index')
    return redirect('recruiters.edit', id=job_id)

@login_required
def delete(request, job_id):
    if not request.user.role == "recruiter":
        return redirect('jobs.index')
    return redirect('recruiters.delete', id=job_id)