#//************************************************************************//#
#//************************************************************************//#
# Author : Chandan Mahto
# Date : 25-10-2018
# Version : 1.0.0
# Changelog : #v 1.0.0 : +added profile view to show the details of
#						 logged in user
#						 +added home view to render the home page of
#						 blog
#						 +added default view to catch all the 'tampered'
#						 urls
#						 +added signup view to enable user signups
#						 +added error view to deal with errors in various views
#						 +added dashboard view for best UI experience
#						 +added success view to deal with success in some views
#						 +added login view to make some use of signup view
#					     +added logout view to free users from their pain
#						 +added create_posts view to prevent boredom of users from
#					      clicking the 4 links on the dashboard.
#						 +added functionality that redirects users to dashboard if
#                         user attempts to view login or signup page after logging in
#			  #v 1.0.1 : users now redirect to dashboard instead of home page if they are
#						 logged in.
#						 +exception handling added for duplicate roll numbers
#						 +added support for user forgetting their passwords
#						 +added show_post view to trash the op for its shitty content
#
#//************************************************************************//#
#//************************************************************************//#

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import signupform, loginform, postform, resetform, commentform, authenticationform
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse
from .models import posts, comments, post_votes, user_request
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import django.contrib.auth as au
from datetime import datetime
import hashlib
import uuid

#//************************************************************************//#

def home(request):
	''' Renders the home.html file to the user
		if the user is not logged in or the dashboard
		if the user is logged in
	'''
	if (request.user.is_authenticated):
		return HttpResponseRedirect(reverse('dashboard'))
	return(render(request,'home/home.html'))

#//************************************************************************//#

def default(request,slug):
	''' renders the home.html file to any wrong
		request that doesn't map to any other view
	'''
	return HttpResponseRedirect(reverse('home'))

#//************************************************************************//#

def signup(request):
	''' renders the signup.html file along with
		an empty signup form for the user to fill and
		send request to create an account.
	'''
	if not request.user.is_authenticated:
		if request.method == 'POST':
			form = signupform(request.POST)
			if form.is_valid():
				try :
					user = User.objects.create_user(username = form.cleaned_data['USERNAME'],
													email = form.cleaned_data['EMAIL'],
													password = form.cleaned_data['PASSWORD'],)
					user.first_name = form.cleaned_data['FIRST_NAME']
					user.last_name = form.cleaned_data['LAST_NAME']
					user.save()
					request.session['task'] = "signup"
				except (IntegrityError) :
					request.session['error'] = "duplicate"
					return HttpResponseRedirect(reverse('error'))
				return HttpResponseRedirect(reverse('success'))
			else :
				return HttpResponseRedirect(reverse('error'))
		else :
			form = signupform()
		return(render(request,'signup/signup.html'))
	else :
		return HttpResponseRedirect(reverse('dashboard'))
#//************************************************************************//#

def error(request):
	''' used to return a simple error response if something doesn't go right in views
	'''
	error = request.session.get('error')
	if error == 'duplicate':
		return HttpResponse('This roll number is already registered is already registered.')
	return HttpResponse('Something went wrong. Visit the homepage at sxcranblog.org')

#//************************************************************************//#
@login_required
def dashboard(request):
	''' renders the dashboard.html for the verified and authenticated user
		it also displays the posts that are recommended for the user
	'''
	if request.user.is_authenticated :
		pass
	else :
		return HttpResponseRedirect(reverse('login'))
	user_posts = posts.objects.all()
	return render(request, 'user/dashboard.html',context = {'user_posts' : user_posts,
															'current_feed' : True})

#//************************************************************************//#

def success(request):
	''' displays a success message on signup and logout tasks
	'''
	task = request.session.get('task')
	if task == "signup":
		del request.session['task']
		return render(request,'misc/success.html', {'link':"login",'message':" to log in to your account",})
	elif task == "logout":
		del request.session['task']
		return render(request,'misc/success.html', {'link':"home",'message':" to return to home",})
	else:
		return HttpResponseRedirect(reverse('error'))

#//************************************************************************//#
def login(request):
	''' performs user login
	'''
	if not request.user.is_authenticated:
		if request.method == "POST":
			form = loginform(request.POST)
			if form.is_valid():
				username = request.POST['USERNAME']
				password = request.POST['PASSWORD']
				#keep_logged = request.POST['KEEP_LOGGED']
				user = au.authenticate(username=username, password=password)
				if (user is not None):
					au.login(request,user)
					request.session['logged'] = True
					return HttpResponseRedirect(reverse('dashboard'))
				else :
					messages.error(request,'username or password not correct')
					return redirect('login')
		else :
			form = loginform()
		return(render(request,'signup/login.html'))
	else :
		return HttpResponseRedirect(reverse('dashboard'))
#//************************************************************************//#
@login_required
def logout(request):
	''' performs user logout
	'''
	try :
		au.logout(request)
		request.session['task'] = "logout"
		request.session['logged'] = False
		return HttpResponseRedirect(reverse('success'))
	except :
		pass
	return HttpResponseRedirect(reverse('home'))

#//************************************************************************//#
@login_required
def create_posts(request):
	''' used to add a new post on the site.
		user enters the post heading and body which is stored along
		with the username of the op(original poster)
	'''
	if request.user.is_authenticated:
		pass
	else :
		return HttpResponseRedirect(reverse('login'))
	if request.method == "POST":
		form = postform(request.POST)
		if form.is_valid():
			heading = request.POST['POST_HEADING']
			body = request.POST['POST_BODY']
			type = request.POST['POST_TYPE']
			if request.user.is_authenticated:
				post = posts.objects.create(post_heading = heading,
											post_op = request.user,
											post_time = datetime.datetime.now(),
											)
				post.post_op_name = request.user.first_name
				post.set_body(body,type)
				post.save()
				return HttpResponseRedirect(reverse('dashboard'))
			else :
				return HttpResponseRedirect(reverse('error'))
	else :
		form = postform()
	return(render(request,'posts/new.html', {'current_post' : True}))

#//************************************************************************//#

def profile(request):
	''' displays the profile.html containing username, name, roll
		and department of the logged in user
	'''
	if request.user.is_authenticated:
		first_name = request.user.first_name
		second_name = request.user.last_name
		username = request.user.username
		email = request.user.email
		return render(request,'user/profile.html',
								{'first_name' : first_name,
								 'last_name' : second_name,
								 'username' : username,
								 'email' : email,
								 'current_profile' : True,
								})
	else :
		return HttpResponseRedirect(reverse('login'))

#//************************************************************************//#

def reset_password(request):
	''' helps in reseting the password of user
	'''
	if request.user.is_authenticated:
		if request == "POST" :
			pass
		else :
			form = resetform()
		return render(request, 'user/reset.html')
	return HttpResponseRedirect(reverse('login'))
#//************************************************************************//#
@login_required
def show_post(request, post_id):
	''' shows the page containing the post and its comments
	'''
	if request.method == "POST":
		if request.user.is_authenticated :
			pass
		else :
			return HttpResponseRedirect(reverse('login'))
		form = commentform(request.POST)
		if form.is_valid():
			body = request.POST['COMMENT_BODY']
			comment = comments.objects.create(comment_op = request.user,
											comment_body = body,
											comment_post = posts.objects.get(id = post_id),
											comment_time = datetime.datetime.now(),
											)
			return redirect(show_post, post_id = post_id)
		else :
			return redirect(show_post, post_id = post_id)
	post = posts.objects.get(id=post_id)
	try :
		comment = comments.objects.filter(comment_post = post_id)
	except :
		return render(request, 'posts/post.html', {'post' : post, 'post_comments': None})
	return render(request,'posts/post.html', {'post': post, 'post_comments' : comment})

#//************************************************************************//#
@login_required
def upvote_post(request):
	''' Used to upvote the posts
	'''
	post_id = request.GET.get('post_id',None)
	upvoted = request.GET.get('upvoted',None)
	post = posts.objects.get(id=post_id)
	pv = post_time(user_id = request.user, post_vote = post, upvoted = upvoted)
	pv.save()
	data = {
		'upvotes' : post.post_upvotes,
		'upvoted' : pv.upvoted
	}
	return JsonResponse(data)

#//************************************************************************//#

def upload_photo(request):
	if request.method == "POST":
		form = imageform(request.POST, request.FILES)
		print('Image received')
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('success'))
		else:
			return HttpResponseRedirect(reverse('error'))
	else:
		form = imageform()
		return render(request,'user/image.html')

#//************************************************************************//#

@require_http_methods(["POST"])
def auth(request):
	form = authenticationform(request.POST)
	if form.is_valid():
		password = form.cleaned_data['PASSWORD']
		username = request.user.username
		user = au.authenticate(username=username, password=password)
		if (user is not None):
			user_token = uuid.uuid4()
			return HttpResponseRedirect(reverse('changepassword', args=[user_token]))
		else :
			return HttpResponseRedirect(reverse('profile'))
	else:
		return HttpResponseRedirect(reverse('profile'))

#//************************************************************************//#

@login_required
def change_password(request,user_token):
	if (True):
		if request.method == 'POST':
			try :
				obj = user_request.objects.get(token = user_token)
				if obj.hash is None:
					raise Exception('error')
				obj.delete()
			except :
				return HttpResponse(status=405)
			form = resetform(request.POST)
			if form.is_valid():
				password = request.POST['PASSWORD']
				request.user.set_password(password)
				request.user.save()
				update_session_auth_hash(request,request.user)
				return redirect(logout)
			else :
				messages.error('Passwords are not same')
				return redirect(change_password,user_token)
		else:
			try :
				obj = user_request.objects.create(token = user_token)
				obj.generate()
			except:
				return HttpResponse(status=405)
			form = resetform()
			return render(request,'user/reset.html', {'user_token' : user_token})
	else :
		return HttpResponse(status=405)

#//************************************************************************//#

def test(request):
	return HttpResponse('Test View')
