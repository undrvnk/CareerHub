# jobs/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from recruiters.models import Post
from profiles.models import Profile
from .forms import ApplicationForm
from math import radians, cos, sin, asin, sqrt

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in miles
    """
    # convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # haversine formula 
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3959  # Radius of earth in miles
    return c * r

# List all jobs
def index(request):
    name_term = request.GET.get('search_name')
    skill_term = request.GET.get('search_skill')
    location_term = request.GET.get('search_location')
    salary_term = request.GET.get('search_salary')
    remote_term = request.GET.get('search_remote')
    visa_term = request.GET.get('search_visa')
    max_distance = request.GET.get('max_distance')
    
    if name_term or skill_term or location_term or salary_term or remote_term or visa_term or max_distance:
        jobs = Post.objects.filter(title__contains=name_term)
        #TODO: make salary range a numeric comparison
        jobs = jobs.filter(location__contains=location_term).filter(salary_range__contains=salary_term).filter(location__contains=remote_term).filter(visa_sponsorship__contains=visa_term)
        #candidates = candidates.filter(education__contains=education_term).filter(work_experience__contains=experience_term)
        if (skill_term):
            jobs = jobs.filter(required_skills__name__contains=skill_term)
    else:
        jobs = Post.objects.all().order_by('-created_at')
    
    #####
    #####
    # Maybe change to map to filter too right now its just a field
    # Filter by distance if user has location and max_distance is specified
    if max_distance:
        try:
            max_distance = float(max_distance)
            # Get current user's profile to check for location
            if request.user.is_authenticated:
                try:
                    user_profile = Profile.objects.get(user=request.user)
                    # Only filter if user has location coordinates
                    if user_profile.lat and user_profile.lng:
                        filtered_jobs = []
                        for job in jobs:
                            # Only include jobs with location data
                            if job.lat and job.lng:
                                distance = haversine_distance(
                                    user_profile.lat, user_profile.lng,
                                    job.lat, job.lng
                                )
                                if distance <= max_distance:
                                    filtered_jobs.append(job)
                        jobs = filtered_jobs
                    else:
                        messages.warning(request, "Your profile doesn't have a location set. Distance filtering requires your location.")
                except Profile.DoesNotExist:
                    messages.warning(request, "You need to create a profile with a location to use distance filtering.")
            else:
                messages.warning(request, "You must be logged in to use distance filtering.")
        except ValueError:
            messages.warning(request, "Invalid distance value.")
    
    return render(request, 'jobs/index.html', {
        'jobs': jobs,
        'max_distance': max_distance,
        'name': name_term,
        'skill': skill_term,
        'location': location_term,
        'salary': salary_term,
        'remote': remote_term,
        'visa': visa_term
    })

# Job detail view and application form
@login_required
def detail(request, job_id):
    job = get_object_or_404(Post, pk=job_id)

    # Check if the user has already applied
    has_applied = Application.objects.filter(job=job, applicant=request.user).exists()
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

# Recommendations for job seekers based on skills
@login_required
def recommendations(request):
    if request.user.role == "recruiter":
        return redirect('recruiters.index')
    
    # Get user's profile and skills
    try:
        profile = request.user.profile
        user_skills = set(profile.skills.all())
    except:
        # If user doesn't have a profile, show message
        messages.info(request, "Please complete your profile to get personalized job recommendations.")
        return render(request, 'jobs/recommendations.html', {'jobs': []})
    
    if not user_skills:
        messages.info(request, "Please add skills to your profile to get personalized job recommendations.")
        return render(request, 'jobs/recommendations.html', {'jobs': []})
    
    # Get all jobs and calculate skill matches
    all_jobs = Post.objects.all()
    
    # Get jobs the user has already applied for
    applied_job_ids = Application.objects.filter(applicant=request.user).values_list('job_id', flat=True)
    
    job_matches = []
    
    for job in all_jobs:
        # Skip jobs the user has already applied for
        if job.id in applied_job_ids:
            continue
            
        job_skills = set(job.required_skills.all())
        if job_skills:  # Only consider jobs with required skills
            matched_skills = user_skills.intersection(job_skills)
            if matched_skills:  # Only show jobs with at least one skill match
                match_count = len(matched_skills)
                match_percentage = (match_count / len(job_skills)) * 100
                job_matches.append({
                    'job': job,
                    'matched_skills': matched_skills,
                    'match_count': match_count,
                    'match_percentage': match_percentage,
                    'total_required': len(job_skills)
                })
    
    # Sort by match percentage (highest first), then by match count
    job_matches.sort(key=lambda x: (x['match_percentage'], x['match_count']), reverse=True)
    
    return render(request, 'jobs/recommendations.html', {'job_matches': job_matches})

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
            job=job,
            applicant=request.user,
            note=note,
            status='applied'
        )
        application.save()
        messages.success(request, f"Successfully applied for {job.title}!")
        return redirect('jobs.detail', job_id=job.id)

    return render(request, 'jobs/apply.html', {'job': job})
