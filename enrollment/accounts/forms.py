from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Please Enter a valid Email Address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Enter Your Name',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',           
        }
        for name, text in placeholders.items():
            self.fields[name].widget.attrs.update({'placeholder': text, 'arial-label': text})
            self.fields[name].label = text
            self.fields[name].help_text = ''
    
    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact =email).exists():
            raise  forms.ValidationError('That Email is already Registered.')
        return email
    
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['username'].widget.attrs.update({'placeholder': 'Email', 'aria-label': 'Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password', 'aria-label': 'Password'})
        self.error_messages['invalid_login'] = 'Email or password is incorrect.'