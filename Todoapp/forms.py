from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields, ModelForm
from Todoapp.models import Todo, Completed
class Newform(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=('username', 'email','password1','password2')

    def save(self, commit=True):
        user= super(Newform, self).save(commit=False)
        user.email= self.cleaned_data['email']
        if commit:
            user.save()
        return user

class Todoform(ModelForm):
    class Meta:
        model=Todo
        fields=['title','description','date','priority']

class Completeform(ModelForm):
    class Meta:
        model=Completed
        fields=['title','description','date','priority']