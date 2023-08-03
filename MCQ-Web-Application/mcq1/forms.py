from django import forms
from .models import Usr
from django.contrib.auth.models import User
from django.forms import ValidationError


class UserForm(forms.ModelForm):
    re_password = forms.CharField(widget=forms.PasswordInput, max_length=50, label='Enter your password again :')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput
        }

    def clean(self):
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['re_password']
        us_name = self.cleaned_data['username']

        for us in User.objects.all(): 
            if us.username == us_name:
                raise ValidationError("Username already taken")

        if pass1!=pass2:
            raise ValidationError("Type the password properly")


class FormName(forms.ModelForm):

    class Meta:
        model = Usr
        fields = ['is_student', 'is_teacher']


    def clean(self):
        student=self.cleaned_data['is_student']
        teacher=self.cleaned_data['is_teacher']

        if student==teacher:
            raise ValidationError("Can't be both student and teacher at the same time nor can you be niether")
