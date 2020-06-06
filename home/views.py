from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model, authenticate
from django.shortcuts import HttpResponseRedirect
from .models import UserProfile
from django.http import HttpResponse
from django.views import View
from store.models import store_user
#from django import form 

def home(request):
    
    return render(request, 'welcome_templates/home.html')

def about(request):

    return render(request, 'welcome_templates/about.html')


class login_page1(View):

    def get(self, request):
        form = LoginForm()
        context = {'form': form}
        return render(request, "welcome_templates/login.html", context=context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                try:
                    shop = store_user.objects.filter(user=user)
                    s_id = (shop[0]).id
                    fail = False
                except:
                    fail = True
                
                if fail == False:
                    return redirect(('/store/home/' + str(s_id)))

                return redirect('/user_social/user_home')
            else:
                print("error.......")
            #send a message to user if their login fails 



#this is where the user data ented on the create acount creates a new user in the databace 

class create_account1(View):

    def get(self, request):
        form = RegisterForm()
        context = {'form': form}
        return render(request, "welcome_templates/create_account.html", context=context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password_first")
            User.objects.create_user(username, email, password)

            new_user = (User.objects.all())
            new_user = new_user[(len(new_user)-1)]
            new_user2 = UserProfile(User = new_user)
            new_user2.save()
            #fix the user creation method here  



#this logs users out 
def logout_page(request):
    
    logout(request)
    return redirect('/')


#need to make ajax responce for a failed atemped at either creating an account or logging in 
#possibly give a real time responce to a misstyped thig in the create account page 