from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model, authenticate
from django.shortcuts import HttpResponseRedirect
from .models import UserProfile
from django.http import HttpResponse




# Create your views here.
def home(request):
    
    return render(request, 'welcome_templates/home.html')

def about(request):

    return render(request, 'welcome_templates/about.html')


#this is where the user data ented on the create acount creates a new user in the databace 
def create_account(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form,
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password_first")
        User.objects.create_user(username, email, password)

        new_user = (User.objects.all())
        new_user = new_user[(len(new_user)-1)]
        new_user2 = UserProfile(user = new_user)
        new_user2.save()
        return render(request, "welcome_templates/new_user.html", {'username': username, 'email':email})

    return render(request, "welcome_templates/create_account.html", context=context)


#this is where users log in 
def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }
    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/user_social/user_home')
        else:
            print("error.......")

    return render(request, "welcome_templates/login.html", context=context)

#this logs users out 
def logout_page(request):
    
    logout(request)
    return redirect('/')


