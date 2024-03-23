from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Category, forum, Reply, Userlike
from .forms import ForumForm, ReplyForm
from visitors.models import Questionvisitor
from django.contrib import messages
from django.core import serializers

from django.core.paginator import Paginator

# Create your views here.


def index(request):
	questionobject = forum.objects.all().order_by('-datetime')
	paginator  = Paginator(questionobject, 3)
	page = request.GET.get('page')
	questions = paginator.get_page(page)

	return render(request, "index.html",{"questions":questions})

def viewquestion(request, pk):
	question = forum.objects.get(id=pk)
	replies = Reply.objects.filter(forum_id=pk)
	try:
		bestreply = Reply.objects.get(id=question.bestreply)
	except Reply.DoesNotExist:
		bestreply = None
	
	form = ReplyForm()
	if not question:
		pass
	else:
		user_ip = request.META.get('REMOTE_ADDR')
		questionvisitorstatus = questionvisitor(forum_id=pk,user_ip=user_ip)
		if questionvisitorstatus == True:
			question.visitor = question.visitor + 1
			question.save()
		return render(request, "viewquestion.html",{"question":question,"replies":replies,"bestreply":bestreply,"form":form}) 

def questionvisitor(forum_id,user_ip):
	forumdata = Questionvisitor.objects.filter(forum_id=forum_id, visitor_ip=user_ip)
	if forumdata:
		return False
	else:
		questionvisitor = Questionvisitor()
		questionvisitor.forum_id = forum_id
		questionvisitor.visitor_ip= user_ip
		questionvisitor.save()

		return True

@login_required(login_url='/login')
def updatereply(request, pk):
	reply = Reply.objects.get(id=pk)
	user = request.user
	description = request.POST['description']
	if user.id == reply.user_id:
		if description:
			reply.description = description
			reply.save()
			messages.success(request, f'Comment Update Successfully')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		else:
			messages.warning(request, f'Filled all the field properly')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		messages.warning(request, f'Error')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def deletereply(request, pk):
	reply = Reply.objects.get(id=pk)
	user = request.user
	dataforum = forum.objects.get(id=reply.forum_id)
	if user.id == reply.user_id:
		reply.delete()
		dataforum.num_reply = dataforum.num_reply - 1
		dataforum.save()
		messages.success(request, f'Comment Delete Successfully')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		messages.warning(request, f'Error')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def replyquestion(request, pk):
	if request.method == 'POST':
		form = ReplyForm(request.POST)
		if form.is_valid():
			forumdata = forum.objects.get(id=pk)
			description = form.cleaned_data['description']
			reply = form.save(commit=False)
			reply.user = request.user
			reply.forum = forumdata
			reply.save()
			forumdata.num_reply = forumdata.num_reply + 1
			forumdata.save()
			messages.success(request, f'Comment Psot Successfully')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		return HttpResponse(form.errors)

@login_required(login_url='/login')
def bestreply(request, pk):
	reply = Reply.objects.get(id=pk)
	forumdata = forum.objects.get(id=reply.forum_id)

	if forumdata.bestreply == reply.id:
		reply.best = False
		reply.save()
		forumdata.bestreply = 0
		forumdata.save()
	else: 
		if forumdata.bestreply != 0:
			oldreply = Reply.objects.get(id=forumdata.bestreply)
			oldreply.best = False
			oldreply.save()
		reply.best = True
		reply.save()
		forumdata.bestreply = reply.id
		forumdata.save()

	messages.success(request, f'Update Successfully')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def likereply(request):
	pk = request.GET.get('pk')
	reply = Reply.objects.get(id=pk)
	user_like = Userlike.objects.filter(reply_id=reply.id, user_id=request.user)

	response_data = {}
	if user_like:
		user_like.delete()
		reply.like = reply.like-1
		reply.save()
	else: 
		user = request.user
		Userlike.objects.create(user_id=user.id, reply_id=reply.id)
		reply.like = reply.like+1
		reply.save()
	
	response_data['like'] = reply.like
	return JsonResponse(response_data, safe=False)



def category(request, pk):
	category = Category.objects.get(id=pk)
	
	questionobject = forum.objects.filter(category_id=category.id)
	paginator  = Paginator(questionobject, 3)
	page = request.GET.get('page')
	questions = paginator.get_page(page)

	return render(request, "category.html",{"category":category,'questions':questions})


@login_required(login_url='/login')
def addquestion(request):
	if request.method == 'POST':
		form = ForumForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			category = form.cleaned_data['category']
			description = form.cleaned_data['description']
			question = form.save(commit=False)
			question.user = request.user
			question.save()
			return redirect('/')
		else:
			return HttpResponse(form.errors)	
	else:
		form = ForumForm()
		return render(request, "addquestion.html",{"form":form})

@login_required(login_url='/login')
def editquestion(request, pk):
	forumdata = forum.objects.get(id=pk)
	form = ForumForm(instance=forumdata)
	return render(request, "editquestion.html",{"form":form})
