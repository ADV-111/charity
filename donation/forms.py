from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='')
    email = forms.EmailField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'e-mail'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            'email': forms.TextInput(attrs={'placeholder': 'e-mail'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Podaj hasło'}),
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': '',
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Hasła nie są takie same'
            )

