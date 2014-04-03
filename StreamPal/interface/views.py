from django.shortcuts import render,redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse 
from django.contrib.auth.decorators import login_required

from interface.forms import UserForm, UserProfileForm
from interface.models import UserProfile 

# Create your views here.
def home_page(request):
	context = RequestContext(request)
	return render_to_response('index.html', 
		{'registered' : request.user.is_authenticated()}, context)

@login_required
def user_home(request):
	context = RequestContext(request)
	return render_to_response('home.html',
		{},
		context)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')


def sign_up(request):
	context = RequestContext(request)

	#Flag to keep tabs if registration is successful
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		#If those are valid...
		if user_form.is_valid() and profile_form.is_valid():
			#Save to database
			user = user_form.save()

			#Hash the password (set_password method does this)
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			#If user supplied picture add to model
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			else:
				profile.picture = "/static/images/default_pic.jpg"

			profile.save()
			registered = True
			new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
			login(request, new_user)
			return render_to_response('home.html',
				{'new_user': True}, context)

		else:
			print user_form.errors, profile_form.errors
			return render_to_response(
				'sign_up.html',
				{'user_form': user_form, 'profile_form': profile_form, 'registered': registered,
				'user_errors': user_form.errors, 'profile_errors': profile_form.errors}, context)

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response(
		'sign_up.html',
		{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
		context)

def user_login(request):
	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		#Django's authentication method
		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/home.html')
			else:
				return HttpResponse('Your account is not currently active.')

		else:
			#This is an incorrect login
			print "Invalid login"
			return HttpResponse("Invalid login details supplied.")

	else:
		#This request is not a POST. 
		return render_to_response('user_login.html', {}, context)
