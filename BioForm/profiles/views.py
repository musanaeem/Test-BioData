#import re
#from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . models import *
from profiles.templates.forms import CreateUserForm, BioForm

#@login_required(login_url = 'login')
def index(request):

    all_user_data = Bio.objects.filter(user_id = request.user)
    context = {
        "users": all_user_data,
    }
    return render(request, "profiles/index.html", context)

def register_user(request):
    #if request.user.is_authenticated:
    #    return redirect('home')

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
    #if request.user.is_authenticated:
    #    return redirect('home')

    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username = email, password = password)
        
        if user is not None:
            login(request, user)
            return redirect("home")
        
        if messages is None:
            messages.info(request, "Username or Password is incorrect")
        
    return render(request, "profiles/login.html")

def logout_user(request):
    logout(request)
    return redirect("login")

#@login_required(login_url = 'login')
def create_record(request):

    if Bio.objects.filter(user_id = request.user.id):
        messages.info(request, "Bio already exists")
        return redirect('home')

    if request.method == "POST":
        form = BioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("home")
    
    form = BioForm()
    form.fields["user"].initial = request.user.id

    context = {
        "form": form,
        "title": "Create Record",
        "heading": "Enter details for the record"
    }

    return render(request, "profiles/create.html", context)

#@login_required(login_url = 'login')
def update_record(request, id):

    selected_user_data = Bio.objects.get(id = id)
    form = BioForm(instance=selected_user_data)

    if request.method == "POST":
            form = BioForm(request.POST, instance=selected_user_data)
            if form.is_valid():
                form.save()
                
                return redirect("home")
    
    context = {
        "form": form,
        "title": "Update Record",
        "heading": "Change the field you want to update"
    }

    return render(request, "profiles/create.html", context)

#@login_required(login_url = 'login')
def delete_record(request, id):
    selected_user_data = Bio.objects.get(id = id)

    if request.method == "POST":
        selected_user_data.delete()
        return redirect("home")
    
    context = {
        "record": selected_user_data
    }

    return render(request, "profiles/delete.html", context)
