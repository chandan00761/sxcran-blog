#//************************************************************************//#
#//************************************************************************//#
# Author : Chandan Mahto
# Date : 25-10-2018
# Version : 1.0.0
# Changelog : #v 1.0.0 : +added signup form to enable user signup 
#						 +added login form to enable user login
#                        +added postform to enable creating and viewing posts
#//************************************************************************//#
#//************************************************************************//#

from django import forms

#//************************************************************************//#

class signupform(forms.Form):
	''' This form is used to get input from the user from signup.html.
		FIRST_NAME = stores the FIRST part of name of student
		LAST_NAME = stores the LAST part of name of student
		USERNAME = ROLL NO is stored
		PASSWORD = PASSWORD
		EMAIL = EMAIL
	'''
	FIRST_NAME = forms.CharField(max_length=30)
	LAST_NAME = forms.CharField(max_length=30)
	USERNAME = forms.CharField(max_length=30)
	PASSWORD = forms.CharField(max_length=30)
	EMAIL = forms.CharField(max_length=150)

#//************************************************************************//#

class loginform(forms.Form):
	''' This form is used to get input from the user from login.html.
		USERNAME = stores the USERNAME of the student
		PASSWORD = stores the PASSWORD of the student
	'''
	USERNAME = forms.CharField(max_length=30)
	PASSWORD = forms.CharField(max_length=30)

#//************************************************************************//#

class postform(forms.Form):
	''' This form is used to get input from the user to create a post.
		POST_HEADING = stores the heading of the post
		POST_HEADING = stores the body of the post
	'''
	POST_HEADING = forms.CharField(max_length=100)
	POST_BODY = forms.CharField(max_length=300)

#//************************************************************************//#
#//************************************************************************//#