from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(label="Full name:")
    email = forms.EmailField(label="E-mail:")

    class Meta:
        model = User
        fields = ("full_name", "email", "username")

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        first_name, last_name = self.cleaned_data["full_name"].split()
        user.first_name = first_name
        user.last_name = last_name
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
