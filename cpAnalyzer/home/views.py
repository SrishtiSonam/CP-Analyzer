from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests
from datetime import datetime, timedelta


# Create your views here.

def home(request):
    context={'page':"CP_Tracker"}
    return render(request, "index.html", context)

def login_page(request):
    context={'page':"Login_Form"}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request,"Please enter the username carefully.")
            return redirect('/login_page/')
        
        user =  authenticate( username=username, password=password)
        if user is None:
            messages.error(request,"Please enter the password carefully.")
            return redirect('/login_page/')
        else:
            login(request,user)
            return render(request, "leaderboard.html")
                
    return render(request, "login_page.html", context)


# ACM - 123
# Admin - Admin


def logout_page(request):
    logout(request)
    return redirect('/login_page/')

def signup_page(request):
    context = {'page': "Signup_Form"}
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup_page/')

        user = User.objects.filter(username = username) 
        if user.exists():
            messages.info(request,'Username already resister.')
            return redirect('/signup_page/')

        user = User.objects.filter(email = email) 
        if user.exists():
            messages.info(request,'Email already resister.')
            return redirect('/signup_page/')

        user = User.objects.create(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('/signup_page/')  

    return render(request, "signup_page.html", context)

def member_form(request):
    context={'page':"Member Form"}
    if request.method == "POST":
        data = request.POST
        rollNo = data.get('rollNo')
        name = data.get('name')
        email = data.get('email')
        codechef_user = data.get('codechef_user')
        codeforces_user = data.get('codeforces_user')
        leetcode_user = data.get('leetcode_user')
        Member.objects.create(
            rollNo=rollNo,
            name=name,
            email=email,
            codechef_user=codechef_user,
            codeforces_user=codeforces_user,
            leetcode_user=leetcode_user,
        )
        messages.success(request, "Member created successfully.")
    return render(request, "member_form.html", context) 

def signup_page(request):
    context = {'page': "Signup_Form"}
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup_page/')

        user = User.objects.filter(username = username) 
        if user.exists():
            messages.info(request,'Username already resister.')
            return redirect('/signup_page/')

        user = User.objects.filter(email = email) 
        if user.exists():
            messages.info(request,'Email already resister.')
            return redirect('/signup_page/')

        user = User.objects.create(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('/signup_page/')  

    return render(request, "signup_page.html", context)
    
@login_required(login_url="/login/")
def leaderboard(request):   
    
    return render(request, "leaderboard.html", context = {'page': "LeaderBoard"})