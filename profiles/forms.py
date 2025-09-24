# profiles/forms.py
from django import forms
from .models import Profile, Skill

class ProfileForm(forms.ModelForm):
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
        fields = ['headline', 'education', 'work_experience', 'gpa', 'links']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Briefly describe yourself'}),
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
        }