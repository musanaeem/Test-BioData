import re
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from . models import *
from profiles.templates.forms import CreateUserForm, BioForm

def index(request):
    form = BioForm()

    if request.method == "POST":
        form = BioForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for" + user)
            return redirect("home")
    
    all_user_data = Bio.objects.all
    context = {
        "users": all_user_data,
        "form": form
    }
    return render(request, "profiles/index.html", context)

def register_user(request):

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for" + user)
            return redirect("login")

    form = CreateUserForm()

    for field in form:
        widget = form.fields[field.name].widget

        widget.attrs['placeholder'] = field.label
        widget.attrs['class'] = 'form-control'
     
    context = {
        "form": form
        }
    return render(request, "profiles/register.html", context)

def login_user(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username,password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home")
        messages.info(request, "Username or Password is incorrect")
        
    return render(request, "profiles/login.html")

def logout_user(request):
    logout(request)
    return redirect("login")