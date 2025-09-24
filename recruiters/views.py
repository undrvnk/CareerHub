from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jobs.models import Job

@login_required
def dashboard(request):
    if not request.user.is_recruiter:
        return redirect('jobs.index')
    jobs = Job.objects.filter(recruiter=request.user).order_by('-created_at')
    return render(request, 'recruiters/dashboard.html', {'jobs': jobs})
