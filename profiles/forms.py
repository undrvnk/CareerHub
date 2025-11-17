# profiles/forms.py
from django import forms
from .models import Profile, Skill

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label='Email Address (for Recruiters to contact you)',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    
    # Custom field for skills input
    skills_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter skills separated by commas'
        })
    )
    
    class Meta:
        model = Profile
        fields = [
            'headline', 'location', 'education', 'work_experience', 'gpa', 'links',
            'profile_visible', 'headline_public', 'skills_public', 'education_public', 
            'gpa_public', 'work_experience_public', 'links_public', 'email_public', 'location_public'
        ]
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Briefly describe yourself'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123 Main St, City, ST'}),
            'education': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your educational background'
            }),
            'gpa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'List your GPA'}),
            'work_experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Describe your work experience'
            }),
            'links': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add relevant links (GitHub, LinkedIn, Portfolio, etc.)'
            }),
            'profile_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'headline_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'skills_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'education_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gpa_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'work_experience_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'links_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'location_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }