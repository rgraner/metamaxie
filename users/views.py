from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm

from .forms import LoginForm, RegistrationForm
from .models import User


def register(request):
    msg = None
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            if new_user is not None and new_user.type==User.Type.MANAGER:
                login(request, new_user)
                msg = 'user created'
                return redirect('scholarships:scholarships_cards')
            if new_user is not None and new_user.type==User.Type.SCHOLAR:
                login(request, new_user)
                msg = 'user created'
                return redirect('profiles:my_profile')              
        else:
            msg = 'form is not valid'
    else:
        form = RegistrationForm()
    
    context = {'form': form, 'msg': msg}
    
    return render(request, 'users/register.html', context )



def login_view(request):
    msg = None
    form = LoginForm(request.POST or None)   
    if request.method=='POST':
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.type==User.Type.MANAGER:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('scholarships:scholarships_cards')
            if user is not None and user.type==User.Type.SCHOLAR:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('profiles:my_profile')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'

    context = {'form': form, 'msg': msg}

    return render(request, 'users/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('users:login')


def change_password(request):
    if request.method!='POST':
        form = PasswordChangeForm(user=request.user)
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            login(request, form.user)
            return redirect('profiles:my_profile')
        else:
            return redirect('users:change_password')

    context = {'form': form}

    return render(request, 'users/change_password.html', context)

