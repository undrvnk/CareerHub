# profiles/admin.py
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'headline', 'education', 'gpa', 'work_experience', 'links', 'skills') # WANT TO INCLUDE DATE CREATED/UPDATED, MAYBE FUTURE
    list_display = ('user', 'headline', 'created_at', 'updated_at')
    search_fields = ('user__username', 'headline')
    list_filter = ('created_at', 'updated_at')