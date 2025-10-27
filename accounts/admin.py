from django.contrib import admin
from accounts.models import User
import csv
from django.http import HttpResponse
from io import StringIO

# Register the User model in the admin interface
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name', 'role', 'email', 
              'password', 'is_staff', 'is_active', 'last_login', 'date_joined') # FIELDS IN ADMIN FORM, ADD STUFF AS NEEDED MAYBE EMAIL AND PW (?)
    list_display = ('username', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('username',)
    actions = ['download_csv']
    def download_csv(self, request, queryset):
        f = StringIO()
        meta = self.model._meta
        field_names = [field.name for field in meta.fields if field.name in ['username', 'first_name', 'last_name', 'role', 'email', 
              'is_staff', 'is_active']]
        writer = csv.writer(f)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Is Staff', 'Is Active', 'Username', 'Role'])
        for job in queryset:
            writer.writerow([getattr(job, field) for field in field_names])
        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=users.csv'
        return response

admin.site.register(User, UserAdmin)
