from django.contrib import admin
from accounts.models import User

# Register the User model in the admin interface
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name', 'role', 'email', 
              'password', 'is_staff', 'is_active', 'last_login', 'date_joined') # FIELDS IN ADMIN FORM, ADD STUFF AS NEEDED MAYBE EMAIL AND PW (?)
    list_display = ('username', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(User, UserAdmin)
