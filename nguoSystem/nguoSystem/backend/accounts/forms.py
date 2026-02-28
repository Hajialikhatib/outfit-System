from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Neno la siri', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Thibitisha neno la siri', widget=forms.PasswordInput)
    is_tailor = forms.BooleanField(
        required=False,
        label='Je, wewe ni mshonaji?',
        help_text='Chagua kama unataka kusajili kama mshonaji'
    )
    tailor_type = forms.ChoiceField(
        choices=(('', '-- Chagua --'), ('kike', 'Nguo za Kike'), ('kiume', 'Nguo za Kiume'), ('zote', 'Zote')),
        required=False,
        label='Aina za nguo unazoshona (kwa washonaji tu)'
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone', 'address', 'gender', 'tailor_type']
        labels = {
            'email': 'Barua pepe',
            'full_name': 'Jina kamili',
            'phone': 'Simu',
            'address': 'Anwani',
            'gender': 'Jinsia',
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Neno la siri hazilingani')
        return p2
    
    def clean(self):
        cleaned_data = super().clean()
        is_tailor = cleaned_data.get('is_tailor')
        tailor_type = cleaned_data.get('tailor_type')
        
        if is_tailor and not tailor_type:
            raise forms.ValidationError('Tafadhali chagua aina ya nguo unazoshona')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        is_tailor = self.cleaned_data.get('is_tailor')
        
        if is_tailor:
            user.is_staff = True
            user.is_approved = False  # Needs admin approval
            user.tailor_type = self.cleaned_data.get('tailor_type')
        else:
            user.is_staff = False
            user.is_approved = True  # Regular users don't need approval
            
        if commit:
            user.save()
        return user
