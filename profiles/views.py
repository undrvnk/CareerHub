from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def view(request):
    return render(request, 'profiles/view.html', {'profile': request.user.profile})

@login_required
def edit(request):
    if request.method == 'POST':
        # Handle profile edit form submission
        return redirect('profiles.view')
    return render(request, 'profiles/edit.html', {'profile': request.user.profile})
