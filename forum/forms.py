from django import forms

from .models import Category, forum, Reply

from django.forms import ModelChoiceField

from .fields import CategoryModelChoiceField

from tinymce.widgets import TinyMCE

class ForumForm(forms.ModelForm):

	categories = Category.objects.all()
	title = forms.CharField()
	category = CategoryModelChoiceField(queryset = categories, to_field_name="id", empty_label="Select Category")
	description = forms.CharField(widget=TinyMCE(attrs={'cols': 10, 'rows': 10}))


	class Meta:
		model = forum
		fields = ('title','category','description')


class ReplyForm(forms.ModelForm):

	description = forms.CharField(widget=TinyMCE(attrs={'cols': 10, 'rows': 10}))

	class Meta:
		model = Reply
		fields = ('description',)



