from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import bcrypt

def index(request):
	if "id" not in request.session:
		request.session["id"] = 0
	return render(request, "logreg/index.html")

def register(request):
	if "valid" not in request.session:
		request.session["valid"] = "Register"
	request.session["valid"] = "Register"
	errors = User.objects.regvalidator(request.POST)
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
		return redirect("/")
	else:
		new_user = User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=bcrypt.hashpw("request.POST['pword']".encode(), bcrypt.gensalt()))
		request.session["id"] = new_user.id
		return redirect("/success")

def login(request):
	if "valid" not in request.session:
		request.session["valid"] = "Login"
	request.session["valid"] = "Login"
	errors = User.objects.logvalidator(request.POST)
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
		return redirect("/")
	login_info = User.objects.get(email=request.POST["email"])
	if login_info == []:
		messages.error(request, "Invalid email or password.")
		return redirect("/")
	elif bcrypt.checkpw("request.POST['pword']".encode(), login_info.password.encode()):
		request.session["id"] = login_info.id
		return redirect("/success")
	else:
		messages.error(request, "Invalid email or password.")
		return redirect("/")

def success(request):
	if request.session["valid"] == "Register":
		messages.success(request, "Successfully registered!")
	elif request.session["valid"] == "Login":
		messages.success(request, "Successfully logged in!")
	context = {
		"user": User.objects.get(id=request.session["id"])
	}
	return render(request, "logreg/success.html", context)
	