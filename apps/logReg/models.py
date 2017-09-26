from __future__ import unicode_literals
from django.db import models
import re
NAME_REGEX = re.compile(r"^[-a-zA-Z']+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

class UserManager(models.Manager):
	def regvalidator(self, postData):
		errors = {}
		if len(postData["first_name"]) < 1:
			errors["first_name"] = "Must enter a first name."
		elif len(postData["first_name"]) < 2:
			errors["first_name"] = "First name must contain at least two characters."
		elif not NAME_REGEX.match(postData["first_name"]):
			errors["first_name"] = "First name contains invalid characters."
		if len(postData["last_name"]) < 1:
			errors["last_name"] = "Must enter a last name."
		elif len(postData["last_name"]) < 2:
			errors["last_name"] = "Last name must contain at least two characters."
		elif not NAME_REGEX.match(postData["last_name"]):
			errors["last_name"] = "Last name contains invalid characters."
		if len(postData["email"]) < 1:
			errors["email"] = "Must enter an email address."
		elif not EMAIL_REGEX.match(postData["email"]):
			errors["email"] = "Email address not valid."
		if User.objects.filter(email=postData["email"]):
			errors["email"] = "Email address is already in use."
		if len(postData["pword"]) < 8:
			errors["pword"] = "Password must contain at least eight characters."
		elif not postData["pword"] == postData["pword_confirm"]:
			errors["pword"] = "Password and confirmation do not match."
		return errors
	def logvalidator(self, postData):
		errors = {}
		if len(postData["email"]) < 1:
			errors["email"] = "Must enter an email address."
		elif not EMAIL_REGEX.match(postData["email"]):
			errors["email"] = "Email address not valid."
		if len(postData["pword"]) < 8:
			errors["pword"] = "Password must contain at least eight characters."
		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()