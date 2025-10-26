from django.db import models
from accounts.models import User

# Create your models here.
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=50)
    body = models.TextField()
    sender = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver+", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)