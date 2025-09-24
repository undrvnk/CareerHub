from django.shortcuts import render

def index(request):
    context = {
        'template_data': {
            'title': 'CareerHub - Find Your Dream Job'
        }
    }
    return render(request, 'home/index.html', context)

def about(request):
    context = {
        'template_data': {
            'title': 'About CareerHub'
        }
    }
    return render(request, 'home/about.html', context)
