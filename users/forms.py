from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User

from .models import Userprofile

from django.contrib.auth.forms import UserCreationForm
from tinymce.widgets import TinyMCE

class UserForm(UserCreationForm):

	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		help_texts = {
		'username': None,
		'email': None,
		'password1': None,
		'password2': None,
		}

class UserprofileForm(forms.ModelForm):

	image = forms.FileField(required=False, widget=forms.FileInput)
	firstname = forms.CharField(required=False)
	lastname = forms.CharField(required=False)
	title = forms.CharField(required=False)
	about = forms.CharField(widget=TinyMCE(attrs={'cols': 10, 'rows': 10}), required=False)


	class Meta:
		model = Userprofile
		fields = [ 'image','firstname', 'lastname', 'title', 'about']
		help_texts = {
		'firstname': None,
		'lastname': None,
		'title': None,
		'about': None,
		}
	


