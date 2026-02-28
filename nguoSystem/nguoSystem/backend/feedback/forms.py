"""
Feedback Forms
==============
Forms for submitting feedback.
"""

from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """Form for submitting feedback on an order."""
    
    class Meta:
        model = Feedback
        fields = ['message', 'rating']
        labels = {
            'message': 'Maoni yako',
            'rating': 'Kiwango cha kuridhika',
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Andika maoni yako kuhusu huduma uliyopata...'
            }),
            'rating': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
        }
