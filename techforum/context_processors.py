from django.shortcuts import render, redirect
from django.template import Context, Template
from forum.models import Category, forum
from blog.models import Blogpost

def categories(request):
 	
 	categories = Category.objects.all()
 	sitequestions = forum.objects.all().order_by('-datetime')[:4:1]
 	siteblogposts = Blogpost.objects.all().order_by('-datetime')[:4:1]


 	return {'categories': categories, 'sitequestions': sitequestions, 'siteblogposts': siteblogposts }
