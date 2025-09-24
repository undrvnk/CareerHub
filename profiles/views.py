# profiles/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Skill
from .forms import ProfileForm

@login_required
def view_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    
    return render(request, 'profiles/view.html', {
        'profile': profile,
        'title': 'My Profile'
    })

@login_required
def edit_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Save profile without committing to handle skills
            profile = form.save(commit=False)
            if not profile.user_id:
                profile.user = request.user
            profile.save()

            # Handle skills
            skills_input = form.cleaned_data.get('skills_input', '')
            if skills_input:
                # Clear existing skills
                profile.skills.clear()
                # Add new skills
                skill_names = [s.strip() for s in skills_input.split(',')]
                for skill_name in skill_names:
                    if skill_name:
                        skill, created = Skill.objects.get_or_create(name=skill_name)
                        profile.skills.add(skill)

            messages.success(request, 'Profile updated successfully!')
            return redirect('profiles.view')
    else:
        initial_data = {}
        if profile:
            initial_data = {
                'headline': profile.headline,
                'education': profile.education,
                'gpa': profile.gpa,
                'work_experience': profile.work_experience,
                'links': profile.links,
                'skills_input': ', '.join(skill.name for skill in profile.skills.all())
            }
        form = ProfileForm(initial=initial_data, instance=profile)

    return render(request, 'profiles/edit.html', {
        'form': form,
        'title': 'Edit Profile'
    })