from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

from .models import Post, Applicant
from jobs.models import Application as JobApplication
from profiles.models import Skill


from profiles.models import Profile

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'recruiters/index.html', {'posts': posts})


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

        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'recruiters/index.html', {'posts': posts})

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
