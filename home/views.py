from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import HttpResponseRedirect

# Create your views here.
def home(request):
    
    return render(request, 'welcome_templates/home.html')

def about(request):

    return render(request, 'welcome_templates/about.html')

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
    return render(request, "welcome_templates/create_account.html", context=context)


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


def logout_page(request):
    
    logout(request)
    return redirect('/')
