# jobs/forms.py
from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    note = forms.CharField(
        required=False,
        label="Optional Note (Tailor your application)",
        widget=forms.Textarea(attrs={
            'rows': 4, 
            'class': 'form-control',
            'placeholder': 'E.g., "I am a strong fit for this role because..."'
        })
    )
    
    class Meta:
        model = Application
        fields = ['note']