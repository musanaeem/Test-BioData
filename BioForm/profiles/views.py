from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . models import *
from profiles.templates.forms import CreateUserForm, BioForm, BlogForm


@login_required(login_url = 'login')
def index(request):

    context = {
        'username': request.user.username,
    }
    return render(request, 'profiles/index.html', context)

def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for' + user)
            return redirect('login')
        

    form = CreateUserForm()

    for field in form:
        widget = form.fields[field.name].widget

        widget.attrs['placeholder'] = field.label
        widget.attrs['class'] = 'form-control'
     
    context = {
        'form': form
    }
    return render(request, 'profiles/register.html', context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        current_user = authenticate(request, username = email, password = password)
        
        if current_user is not None:
            login(request, current_user)
            return redirect('home')
        
        messages.info(request, 'Username or Password is incorrect')
        
    return render(request, 'profiles/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url = 'login')
def bio_view(request):
    user_data = Bio.objects.filter(user_id = request.user)
    context = {
        'users': user_data,
    }
    return render(request, 'profiles/bio.html', context)
    

@login_required(login_url = 'login')
def blog_list_view(request):

    blogs = Blog.objects.all()

    context = {
        'username': request.user.username,
        'blogs': blogs
    }
    return render(request, 'profiles/blogs.html', context)

@login_required(login_url = 'login')
def blog_view(request, id):

    blog = Blog.objects.get(id=id)

    context = {
        'username': request.user.username,
        'blog': blog
    }
    return render(request, 'profiles/blog.html', context)

@login_required(login_url = 'login')
def bio_create(request):

    if Bio.objects.filter(user_id = request.user.id):
        messages.info(request, 'Bio already exists')
        return redirect('home')

    if request.method == 'POST':        
        form = BioForm(request.POST)

        if form.is_valid():
            form.cleaned_data['user'] = request.user.id
            form.save()
            return redirect('home')
    
    form = BioForm()
    form.fields['user'].initial = request.user.id

    context = {
        'form': form,
        'title': 'Create Record',
        'heading': 'Enter details for the record'
    }

    return render(request, 'profiles/create.html', context)

@login_required(login_url = 'login')
def blog_create(request):

    if request.method == 'POST':        
        form = BlogForm(request.POST)

        if form.is_valid():
            form.cleaned_data['user'] = request.user.id
            form.save()
            return redirect('blogs')
    
    form = BlogForm()
    form.fields['user'].initial = request.user.id

    context = {
        'form': form,
        'title': 'Create New Blog'
    }

    return render(request, 'profiles/create.html', context)

@login_required(login_url = 'login')
def bio_update(request, id):

    selected_user_data = Bio.objects.get(id = id)
    form = BioForm(instance=selected_user_data)

    if request.method == 'POST':
            form = BioForm(request.POST, instance=selected_user_data)
            if form.is_valid():
                form.save()
                
                return redirect('home')
    
    context = {
        'form': form,
        'title': 'Update Record',
        'heading': 'Change the field you want to update'
    }

    return render(request, 'profiles/create.html', context)

@login_required(login_url = 'login')
def blog_update(request, id):

    selected_user_data = Blog.objects.get(id = id)
    form = BlogForm(instance=selected_user_data)

    if request.method == 'POST':
            form = BlogForm(request.POST, instance=selected_user_data)
            if form.is_valid():
                form.save()
                
                return redirect('blogs')
    
    context = {
        'form': form,
        'title': 'Update Blog',
    }

    return render(request, 'profiles/create.html', context)

@login_required(login_url = 'login')
def bio_delete(request, id):
    selected_user_data = Bio.objects.get(id = id)

    if request.method == 'POST':
        selected_user_data.delete()
        return redirect('home')
    
    context = {
        'record': selected_user_data
    }

    return render(request, 'profiles/delete.html', context)

@login_required(login_url = 'login')
def blog_delete(request, id):
    selected_user_data = Blog.objects.get(id = id)

    if request.method == 'POST':
        selected_user_data.delete()
        return redirect('blogs')
    
    context = {
        'record': selected_user_data
    }

    return render(request, 'profiles/delete.html', context)
