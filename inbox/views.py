from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from accounts.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    inbox = Message.objects.all().filter(receiver=request.user).order_by('-created_at')
    return render(request, 'inbox/index.html', {'inbox': inbox})

@login_required
def compose(request, id):
    receiver = get_object_or_404(User, pk=id)

    if request.method == 'POST':
        message = Message(
            subject=request.POST['subject'],
            body=request.POST['body'],
            sender=request.user.first_name + " " + request.user.last_name,
            receiver=receiver,
        )
        message.save()

        inbox = Message.objects.all().filter(receiver=request.user).order_by('-created_at')
        return render(request, 'inbox/index.html', {'inbox': inbox})
    
    return render(request, 'inbox/compose.html', {'receiver': receiver})
