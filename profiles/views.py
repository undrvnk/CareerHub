# profiles/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
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
            try:
                with transaction.atomic():
                    # 1. Manually handle the email field from the form
                    new_email = form.cleaned_data['email']
                    if request.user.email != new_email:
                        request.user.email = new_email
                        request.user.save()

                    # 2. Save the Profile (ModelForm handles Profile fields)
                    profile = form.save(commit=False)
                    if not profile.user_id:
                        profile.user = request.user
                    
                    # 3. Handle location coordinates
                    lat = request.POST.get('lat')
                    lng = request.POST.get('lng')
                    profile.lat = float(lat) if lat else None
                    profile.lng = float(lng) if lng else None
                    
                    profile.save()

                    # 4. Handle skills (Many-to-Many field)
                    skills_input = form.cleaned_data.get('skills_input', '')
                    if skills_input:
                        profile.skills.clear()
                        skill_names = [s.strip() for s in skills_input.split(',')]
                        for skill_name in skill_names:
                            if skill_name:
                                skill, created = Skill.objects.get_or_create(name=skill_name)
                                profile.skills.add(skill)

                messages.success(request, 'Profile updated successfully! 🚀')
                return redirect('profiles.view')
            except Exception as e:
                messages.error(request, f'An unexpected error occurred while saving: {e}')
                # Fall through to re-render form with errors
        # If form is invalid, fall through to re-render them with errors
        
    else: # GET request
        initial_data = {
            'email': request.user.email, # <-- Add initial email value from User
        }
        if profile:
            initial_data.update({
                'skills_input': ', '.join(skill.name for skill in profile.skills.all()),
            })
        
        form = ProfileForm(initial=initial_data, instance=profile)
    
    # Ensure skills_input has initial data even if form is not bound
    if profile and request.method == 'GET':
        form.fields['skills_input'].initial = ', '.join(skill.name for skill in profile.skills.all())

    return render(request, 'profiles/edit.html', {
        'form': form,
        'profile': profile,
        'title': 'Edit Profile'
    })