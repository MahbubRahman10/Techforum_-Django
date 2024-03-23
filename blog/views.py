from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Blogpost, Blogcomment

from django.core.paginator import Paginator

from .forms import BlogcommentForm

from django.contrib import messages

# Create your views here.

def index(request):
	blogpostobject = Blogpost.objects.all().order_by('-datetime')
	paginator = Paginator(blogpostobject, 3)
	page = request.GET.get('page')
	blogs = paginator.get_page(page)

	return render(request, 'blog/index.html', {'blogs': blogs})

def viewpost(request, pk):
	blog = Blogpost.objects.get(id=pk)
	form = BlogcommentForm()
	blogcomments = Blogcomment.objects.filter(blogpost_id=pk)
	return render(request, 'blog/viewpost.html', {'blog': blog, 'form': form, 'blogcomments': blogcomments})


def blogcomment(request, pk):
	if request.method == 'POST':
		form = BlogcommentForm(request.POST)
		if form.is_valid():
			blogpost = Blogpost.objects.get(id=pk)
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			description = form.cleaned_data['description']
			comment = form.save(commit=False)
			comment.user = request.user
			comment.blogpost = blogpost
			comment.save()
			messages.success(request, f'Comment Post Successfully')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		return HttpResponse(form.errors)