# jobs/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from recruiters.models import Post
from .forms import ApplicationForm

# List all jobs
def index(request):
    jobs = Post.objects.all().order_by('-created_at')
    return render(request, 'jobs/index.html', {'jobs': jobs})

# Job detail view and application form
@login_required
def detail(request, job_id):
    job = get_object_or_404(Post, pk=job_id)

    # Check if the user has already applied
    has_applied = Application.objects.filter(post=job, applicant=request.user).exists()
    is_recruiter = request.user.role == 'recruiter'

    if request.method == 'POST':
        if is_recruiter or has_applied:
            messages.error(request, "Cannot apply for this job.")
            return redirect('jobs.detail', job_id=job.id)

        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = Application(
                post=job,
                applicant=request.user,
                note=form.cleaned_data['note'],
                status='applied'
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

# Show applications submitted by the logged-in job seeker
@login_required
def applications(request):
    if request.user.role == "recruiter":
        return redirect('recruiters.index')

    user_applications = Application.objects.filter(applicant=request.user)
    return render(request, 'jobs/applications.html', {'applications': user_applications})

# Redirect recruiter create/edit/delete actions to recruiters app
@login_required
def create(request):
    if request.user.role != "recruiter":
        return redirect('jobs.index')
    return redirect('recruiters.create')

@login_required
def edit(request, job_id):
    if request.user.role != "recruiter":
        return redirect('jobs.index')
    return redirect('recruiters.edit', id=job_id)

@login_required
def delete(request, job_id):
    if request.user.role != "recruiter":
        return redirect('jobs.index')
    job = get_object_or_404(Post, pk=job_id)
    if request.method == 'POST':
        job.delete()
        messages.success(request, f"{job.title} deleted successfully.")
        return redirect('jobs.index')
    return render(request, 'jobs/delete.html', {'job': job})

# View all applications for a job (recruiter view)
@login_required
def view_applications(request, job_id):
    if request.user.role != "recruiter":
        return redirect('jobs.index')

    job = get_object_or_404(Post, pk=job_id)
    applications = Application.objects.filter(post=job)
    return render(request, 'jobs/view_applications.html', {'job': job, 'applications': applications})

# Apply for a job (alternative view)
@login_required
def apply(request, job_id):
    if request.user.role == "recruiter":
        return redirect('accounts.login')

    job = get_object_or_404(Post, pk=job_id)

    if request.method == 'POST':
        note = request.POST.get('note', '')

        # Prevent duplicate applications
        if Application.objects.filter(post=job, applicant=request.user).exists():
            messages.error(request, "You have already applied for this job.")
            return redirect('jobs.detail', job_id=job.id)

        application = Application(
            post=job,
            applicant=request.user,
            note=note,
            status='applied'
        )
        application.save()
        messages.success(request, f"Successfully applied for {job.title}!")
        return redirect('jobs.detail', job_id=job.id)

    return render(request, 'jobs/apply.html', {'job': job})
