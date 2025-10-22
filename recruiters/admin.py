from django.contrib import admin
from .models import Post, Applicant, PostAdmin, ApplicantAdmin
# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Applicant, ApplicantAdmin)