from django import forms
from django.forms import ModelForm

from .models import Blogcomment

from tinymce.widgets import TinyMCE


class BlogcommentForm(forms.ModelForm):

	name = forms.CharField()
	email = forms.CharField()
	description = forms.CharField(widget=TinyMCE(attrs={'cols': 5, 'rows': 5}))

	class Meta:
		model =  Blogcomment
		fields = ('name', 'email', 'description')


