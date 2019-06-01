#//************************************************************************//#
#//************************************************************************//#
# Author : Chandan Mahto
# Date : 25-10-2018
# Version : 1.0.0
# Changelog : #v 1.0.0 : +added posts model to store posts and manage them
#			  #v 1.1.0 : +added comment model to store comments and manage them
#//************************************************************************//#
#//************************************************************************//#

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
import hashlib

#//************************************************************************//#

class posts(models.Model):
	''' post_heading = VARCHAR field to store the heading of a post of max length 150.
					   cannot be a null or empty value
		post_body = VARCHAR field to store the body of the post.
					cannot be null or empty.
		post_op = Foreign Key which maps the User table to the posts table in a one to many
				  relationship
	'''
	post_types = (
		('T','Text Post'),
		('M', 'Media Post'),
		('U', 'URL Post')
	)
	post_op = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
	post_op_name = models.CharField(max_length=150, null=False, default = "Anonymous")
	post_heading = models.CharField(max_length=150, null=False)
	post_type = models.CharField(max_length=1, choices = post_types, null=False,  default = 'T')
	post_body = models.CharField(max_length = 1000, blank=False, null=True, default=None)
	post_url = models.URLField(max_length=200, blank=False, null=True, default= None)
	post_upvotes = models.IntegerField(default = 0)
	post_time = models.DateTimeField(default = datetime.now())
	def set_body(self, value, type):
		if type=='text':
			self.post_body = value
			self.post_type = 'T'
		elif type=='media':
			self.post_url = value
			self.post_type = 'M'
		else:
			self.post_url = value
			self.post_type = 'U'
	def upvote(self):
		self.post_upvotes = self.post_upvotes + 1
	def downvote(self):
		self.post_upvotes = self.post_upvotes - 1
#//************************************************************************//#

class comments(models.Model):
	comment_op = models.ForeignKey(User,on_delete = models.CASCADE, null = True)
	comment_body = models.CharField(max_length=150, null=False)
	comment_post = models.ForeignKey(posts, on_delete = models.CASCADE, null=True)
	commment_upvotes = models.IntegerField(default = 0)
	comment_time = models.DateTimeField(default = datetime.now())

#//************************************************************************//#

class post_votes(models.Model):
	''' Manage the upvotes of the users on the posts
	'''
	user_id = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
	post_vote = models.ForeignKey(posts, on_delete = models.CASCADE, null=True)
	upvoted = models.BooleanField(default = True)

	class Meta:
		unique_together = ['user_id','post_vote']

	def save(self, *args, **kwargs):
		if self.upvoted :
			self.post_vote.upvote()
		else :
			self.post_vote.downvote()
		self.post_vote.save()
		super().save(*args,**kwargs)

#//************************************************************************//#

class user_request(models.Model):
	token = models.CharField(max_length=64,primary_key=True)
	hash = models.CharField(max_length=64,default=None,null=True)

	class Meta:
		unique_together = ['token','hash']

	def validate(self):
		pass

	def generate(self):
		self.token = self.token
		hasher = hashlib.sha256()
		hasher.update(str.encode(self.token))
		hasher.update(str.encode(str(datetime.now())))
		self.hash = hasher.hexdigest()
		self.save()
