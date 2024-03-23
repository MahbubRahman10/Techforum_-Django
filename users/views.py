from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, UserprofileForm
from .models import Userprofile

from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User, auth
from django.core.mail import EmailMessage

from django.contrib import messages

from forum.models import forum, Reply

from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.

def register(request):
	if request.user.is_authenticated:
		return redirect("Home-Page")
	else:
		if request.method == "POST":
			form = UserForm(request.POST)
			if form.is_valid():
				user = form.save(commit=False)
				user.is_active = False
				user.save()
				current_site = get_current_site(request)
				mail_subject = 'Activate your Account.'
				message = render_to_string('acc_active_email.html', {
	                'user': user,
	                'domain': current_site.domain,
	                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
	                'token':account_activation_token.make_token(user),
	            })
				to_email = form.cleaned_data.get('email')
				email = EmailMessage(mail_subject,message,to=[to_email])
				email.send()

				messages.success(request, f'Please confirm your email address to complete the registration')

				return redirect('Register-Page')

		else:
			form = UserForm()
			return render(request, "register.html", {'form':form})

		return render(request, "register.html", {'form':form})


def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username = username, password = password)

		if user is not None:
			auth.login(request, user)
			if 'remember' in request.POST:
				request.session.set_expiry(0)
			return redirect('Home-Page')
		else:
			messages.warning(request, f'Invalid credentials')
			return redirect('Login-Page')
	else:
		return render(request,"login.html")

def logout(request):
	auth.logout(request)
	return redirect("Home-Page")


def activate(request, uidb64, token):


    try:
		
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        auth.login(request, user)

        Userprofile.objects.create(user=user) 
       

        return redirect("Home-Page")
    else:
    	messages.warning(request, f'Activation link is invalid!')
    	return redirect('Register-Page')
		


def passwordreset(request):
	if request.method == 'POST':
		pass
	else:
		return render(request, 'reset.html')


def userprofile(request, pk):
	users = User.objects.get(id=pk)
	return render(request, 'userprofile.html', {'pk':pk, 'users':users})

def userquestion(request, pk):
	users = User.objects.get(id=pk)
	questions = forum.objects.filter(user_id=pk)
	replies = Reply.objects.filter(user_id=pk)
	return render(request, 'userquestion.html', {'pk':pk, 'questions':questions,'replies': replies, 'users': users})

@login_required(login_url='/login')
def profilesetting(request, pk):
	userprofile = get_object_or_404(Userprofile, user_id=pk)
	user = User.objects.get(id=pk)
	if request.method == 'POST':
		form = UserprofileForm(request.POST, request.FILES)
		if form.is_valid():
			userprofile.image = form.cleaned_data['image']
			userprofile.firstname = form.cleaned_data['firstname']
			userprofile.lastname = form.cleaned_data['lastname']
			userprofile.title = form.cleaned_data['title']
			userprofile.about = form.cleaned_data['about']
			userprofile.save()
			messages.success(request, f'Update Successfully')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

	else:
		form = UserprofileForm(instance=userprofile)

	return render(request, 'profilesetting.html', {'pk':pk, 'form': form,'userprofile':user})

@login_required(login_url='/login')
def passwordsetting(request, pk):
	users = get_object_or_404(User, id=pk)
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, f'Your password was successfully updated!')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		else:
			messages.error(request, f'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)

	return render(request, 'passwordsetting.html', {'users':users, 'pk':pk, 'form':form})


def error_404_view(request, exception):
	return render(request,'404.html')

def error_500_view(request, exception):
	return render(request,'500.html')