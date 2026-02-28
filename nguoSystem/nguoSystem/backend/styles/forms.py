from django import forms
from .models import Style


class StyleForm(forms.ModelForm):
    """Form for creating and editing clothing styles"""
    
    class Meta:
        model = Style
        fields = ['name', 'description', 'price', 'gender', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Andika jina la mtindo'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Andika maelezo ya mtindo',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bei kwa TSh',
                'step': '0.01'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'name': 'Jina la Mtindo',
            'description': 'Maelezo',
            'price': 'Bei (TSh)',
            'gender': 'Jinsia',
            'category': 'Aina',
            'image': 'Picha ya Nguo'
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('Bei lazima iwe zaidi ya sifuri')
        return price
