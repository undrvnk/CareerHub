import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
# Import for emailing
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .models import Post, Applicant, SavedSearch
from jobs.models import Application as JobApplication
from profiles.models import Skill
from profiles.models import Profile # <--- REQUIRED FOR MAP
from accounts.models import User as UserAccount

def index(request):
    # Recruiters should only see their own job postings
    if request.user.is_authenticated and request.user.role == "recruiter":
        posts = Post.objects.filter(recruiter=request.user).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    return render(request, 'recruiters/index.html', {'posts': posts})


@login_required
@require_POST
def email_candidate(request):
    if request.user.role != "recruiter":
        print('not recruiter')
        messages.error(request, "Access denied. Only recruiters can email candidates.")
        return redirect('recruiters.index')

    # Get data from the POST request
    candidate_email = request.POST.get('candidate_email')
    subject = request.POST.get('subject')
    message_body = request.POST.get('message_body')
    recruiter_email = request.POST.get('recruiter_email')
    
    # TODO: Paste your CareerHub app password here
    careerhub_password = 'gthc tyyu chmx agnt'  # App password for cs2340careerhub@gmail.com
    
    # Get redirect URL from hidden field
    redirect_url = request.POST.get('redirect_url', request.META.get('HTTP_REFERER', '/'))

    if not all([candidate_email, subject, message_body]):
        print('missing fields')
        messages.error(request, "Missing fields: Email, Subject, and Message Body are required.")
        return redirect(redirect_url)
    
    # Simple email validation check (for safety)
    if '@' not in candidate_email or '.' not in candidate_email:
        messages.error(request, "Invalid candidate email address.")
        return redirect(redirect_url)

    try:
        # Construct the email body, including recruiter's details
        recruiter_name = f"{request.user.first_name} {request.user.last_name}"
        full_message = f"\n\n{message_body}\n\n---\n"
        msg = MIMEMultipart()
        msg['From'] = 'cs2340careerhub@gmail.com'
        msg['To'] = candidate_email
        msg['Cc'] = recruiter_email  # CC the recruiter
        msg['Subject'] = subject
        msg.attach(MIMEText(full_message, 'plain'))
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls(context=ssl.create_default_context())
            server.login('cs2340careerhub@gmail.com', careerhub_password)
            # Send to both candidate and recruiter (via CC)
            server.sendmail('cs2340careerhub@gmail.com', [candidate_email, recruiter_email], msg.as_string())
        print("Success")
        messages.success(request, f"Email sent successfully to {candidate_email} (with CC to {recruiter_email})!")
    except Exception as e:
        print(e)
        messages.error(request, f"Failed to send email: {e}")

    return redirect(redirect_url)

@login_required
def create(request):
    if request.user.role != "recruiter":
        return redirect('recruiters.index')

    if request.method == 'POST':
        post = Post(
            title=request.POST['title'],
            company=request.POST['company'],
            description=request.POST['description'],
            location=request.POST['location'],
            salary_range=request.POST['salary_range'],
            visa_sponsorship=request.POST['visa_sponsorship'],
            recruiter=request.user,
        )
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        post.lat = float(lat) if lat else None
        post.lng = float(lng) if lng else None
        post.save()

        skills_input = request.POST.get("required_skills", "")
        skills = [s.strip() for s in skills_input.split(",") if s.strip()]
        for skill_name in skills:
            skill, _ = Skill.objects.get_or_create(name=skill_name)
            post.required_skills.add(skill)

        return redirect('recruiters.index')

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
    valid_search = name_term or skill_term or education_term or experience_term
    if valid_search:
        candidates = Profile.objects.filter(user__first_name__contains=name_term) | Profile.objects.filter(user__last_name__contains=name_term)
        candidates = candidates.filter(education__contains=education_term).filter(work_experience__contains=experience_term)
        if (skill_term):
            candidates = candidates.filter(skills__name__contains=skill_term)
    else:
        candidates = Profile.objects.all().order_by('-created_at')
    
    # Filter out profiles that are hidden from recruiters
    candidates = candidates.filter(profile_visible=True)
    #candidates = Profile.objects.all().order_by('-created_at')

    results = candidates.__len__
    search_id = request.GET.get('search_id')

    saved_searches = SavedSearch.objects.filter(user=request.user)
    for search in saved_searches:
        search_results = Profile.objects.filter(user__first_name__contains=search.name) | Profile.objects.filter(user__last_name__contains=search.name)
        search_results = search_results.filter(education__contains=search.education).filter(work_experience__contains=search.experience)
        if (search.skill):
            search_results = search_results.filter(skills__name__contains=search.skill)
        # Also filter out hidden profiles from saved search results
        search_results = search_results.filter(profile_visible=True)
        search.new_results = (search_results.count())
        search.save()
    
    if search_id:
        current_search = SavedSearch.objects.get(id=search_id)
        current_search.result_count = current_search.new_results
        current_search.save()
    return render(request, 'recruiters/candidates.html', {
        'candidates': candidates,
        'valid_search': valid_search,
        'name': name_term,
        'skill': skill_term,
        'education': education_term,
        'experience': experience_term,
        'results': results,
        'saved_searches': saved_searches
    })

def detail(request, job_id):
    post = get_object_or_404(Post, pk=job_id)
    return render(request, 'posts/detail.html', {'post': post})

@login_required
def edit(request, id):
    if request.user.role != "recruiter":
        return redirect('recruiters.index')

    post = get_object_or_404(Post, pk=id)

    if request.method == 'POST':
        post.title = request.POST['title']
        post.company = request.POST['company']
        post.description = request.POST['description']
        post.location = request.POST['location']
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        post.lat = float(lat) if lat else None
        post.lng = float(lng) if lng else None
        post.salary_range = request.POST['salary_range']
        post.recruiter = request.user
        post.save()
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'recruiters/index.html', {'posts': posts})

    return render(request, 'recruiters/edit.html', {'post': post})


@login_required
def delete(request, id):
    if request.user.role != "recruiter":
        return redirect('recruiters.index')

    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('recruiters.index')


@login_required
def detail(request, id):
    post = get_object_or_404(Post, id=id)

    # --- START: Applicant Map Data Logic (NEW/MODIFIED) ---
    applicant_users = JobApplication.objects.filter(job=post).values_list('applicant__id', flat=True).distinct()

    candidate_locations = Profile.objects.filter(
        user__id__in=applicant_users,
        location_public=True,
        lat__isnull=False,
        lng__isnull=False
    ).values('user__first_name', 'user__last_name', 'lat', 'lng')
    
    applicant_map_data = list(candidate_locations)
    # --- END: Applicant Map Data Logic ---


    applicants = Applicant.objects.filter(post=post).order_by('-applied_at')
    job_applications = JobApplication.objects.filter(job=post).order_by('-created_at')

    stages = ['applied', 'interview', 'offer', 'hired']
    unified = {stage: [] for stage in stages}

    for a in applicants:
        entry = {
            'username': a.name,
            'status': a.stage,
            'created_at': a.applied_at,
            'applicant_id': a.id,
            'source': 'recruiter',
        }
        key = a.stage.lower()
        unified.setdefault(key, []).append(entry)

    for app in job_applications:
        key = (app.status or '').lower()
        entry = {
            'username': getattr(app.applicant, 'username', str(app.applicant)),
            'status': app.status,
            'created_at': app.created_at,
            'applicant_id': getattr(app.applicant, 'id', None),
            'source': 'job',
        }
        if key in unified:
            unified[key].append(entry)
        else:
            unified['applied'].append(entry)

    applicants_by_stage_list = [(stage, unified.get(stage, [])) for stage in stages]

    return render(request, 'recruiters/detail.html', {
        'post': post,
        'stages': stages,
        'applicants_by_stage_list': applicants_by_stage_list,
        'applicant_map_data_json': json.dumps(applicant_map_data), # <--- Map data context
    })


@login_required
@require_POST
def move_application(request):
    post_id = request.POST.get('post_id')
    target = request.POST.get('target_stage')
    username = request.POST.get('username')
    applicant_id = request.POST.get('applicant_id')

    if not post_id or not target:
        return JsonResponse({'ok': False, 'error': 'missing post_id or target_stage'}, status=400)

    post = get_object_or_404(Post, id=post_id)

    user = None
    if applicant_id:
        User = get_user_model()
        try:
            user = User.objects.get(id=applicant_id)
        except User.DoesNotExist:
            pass

    if not user and username:
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass

    if user:
        # JobApplication uses field name 'job' for the FK to Post
        job_app = JobApplication.objects.filter(job=post, applicant=user).first()
        if job_app:
            # Normalize target to the allowed status keys used by the model
            allowed = [c[0] for c in JobApplication.STATUS_CHOICES]
            t = (target or '').lower()
            # Map UI 'hired' to backend 'closed' if necessary
            if t == 'hired' and 'closed' in allowed:
                t = 'closed'
            if t in allowed:
                job_app.status = t
                job_app.save()
                return JsonResponse({'ok': True})
            else:
                return JsonResponse({'ok': False, 'error': f"invalid target '{target}'. allowed: {allowed}"}, status=400)

    # fallback: recruiters.Applicant
    if applicant_id:
        appq = Applicant.objects.filter(post=post, id=applicant_id)
    elif username:
        appq = Applicant.objects.filter(post=post, name=username)
    else:
        appq = Applicant.objects.none()

    if appq.exists():
        a = appq.first()
        a.stage = target.lower()
        a.save()
        return JsonResponse({'ok': True})

    return JsonResponse({'ok': False, 'error': 'application not found'}, status=404)


@login_required
def recommendations(request):
    """
    Recommends candidates for the recruiter's job postings based on skill match.
    Excludes candidates who have already applied to the specific job.
    """
    if request.user.role != "recruiter":
        return redirect('jobs.index')
    
    # Get all job postings by this recruiter
    my_posts = Post.objects.filter(recruiter=request.user)
    
    if not my_posts.exists():
        return render(request, 'recruiters/recommendations.html', {'recommendations': []})
    
    # Get all candidates with profiles, only those with visible profiles
    candidates = Profile.objects.select_related('user').prefetch_related('skills').filter(profile_visible=True)
    
    recommendations = []
    
    for candidate in candidates:
        candidate_skills = set(candidate.skills.all())
        if not candidate_skills:
            continue  # Skip candidates without skills
        
        # Find best matching job for this candidate
        best_match = None
        best_match_data = None
        
        for post in my_posts:
            # Check if candidate has already applied to this specific job
            has_applied = JobApplication.objects.filter(
                job=post, 
                applicant=candidate.user
            ).exists()
            
            if has_applied:
                continue  # Skip this job for this candidate
            
            post_skills = set(post.required_skills.all())
            if not post_skills:
                continue  # Skip jobs without required skills
            
            matched_skills = candidate_skills.intersection(post_skills)
            if matched_skills:  # Only consider if there's at least one skill match
                match_count = len(matched_skills)
                match_percentage = (match_count / len(post_skills)) * 100
                
                # Keep track of the best match for this candidate
                if best_match is None or match_percentage > best_match_data['match_percentage']:
                    best_match = post
                    best_match_data = {
                        'job': post,
                        'matched_skills': matched_skills,
                        'match_count': match_count,
                        'match_percentage': match_percentage,
                        'total_required': len(post_skills)
                    }
        
        # Add candidate if they have at least one matching job
        if best_match_data:
            recommendations.append({
                'candidate': candidate,
                'best_match': best_match_data
            })
    
    # Sort by match percentage (highest first), then by match count
    recommendations.sort(
        key=lambda x: (x['best_match']['match_percentage'], x['best_match']['match_count']), 
        reverse=True
    )
    
    return render(request, 'recruiters/recommendations.html', {'recommendations': recommendations})

@login_required
def save_search(request):
    name = request.GET.get('name')
    skill = request.GET.get('skill')
    education = request.GET.get('education')
    experience = request.GET.get('experience')
    if name or skill or education or experience:
        saved = SavedSearch(
            name = name,
            skill = skill,
            education = education,
            experience = experience,
            user = request.user,
            result_count = request.GET.get('results'),
            new_results = request.GET.get('results')
        )
        saved.save()
    return redirect('recruiters.candidates')

@login_required
def delete_search(request, id):
    search = SavedSearch.objects.get(id=id)
    if search.user == request.user:
        search.delete()
    return redirect('recruiters.candidates')