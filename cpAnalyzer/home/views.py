from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.decorators import login_required
from django_otp.util import random_hex
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .tests import *


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
            members = Member.objects.all()
            codechef_list = [member.codechef_user for member in members]
            codeforces_list = [member.codeforces_user for member in members]
            for member in members:
                member.codeforces_problem = codeforces_problems_solved(member.codeforces_user)
                member.codeforces_rating = codeforces_rating(member.codeforces_user)
                member.codeforces_recent = f"https://codeforces.com/submissions/{member.codeforces_user}"
                member.codechef_problem = codechef_problems_solved(member.codechef_user)
                member.codechef_rating = codechef_rating(member.codechef_user)
                # member.codechef_recent = f"https://codeforces.com/submissions/{codechef_user}"
                member.total_problem = total_problems_solved(member.codeforces_user,member.codechef_user)
            return render(request, "leaderboard.html", context = {'page': "LeaderBorad",'codechef_list':codechef_list,'codeforces_list':codeforces_list,'members': members})

                
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
    

# ----------------------------------------------------views.py


def send_otp(request):
    user = request.user

    # Generate a new secret key and create or update the OTPVerification instance.
    otp_secret_key = random_hex(20)
    otp_verification, _ = OTPVerification.objects.update_or_create(
        user=user, defaults={'secret_key': otp_secret_key}
    )

    # Send the OTP to the user through their preferred method (e.g., SMS, Email).
    # For demonstration purposes, we'll simply print the OTP here.
    otp = str(random.randint(100000, 999999))
    print(f"Your OTP: {otp}")

    # Save the OTP to the TOTPDevice for verification later.
    TOTPDevice.objects.create(user=user, tolerance=1, secret=otp)

    return render(request, 'otp_sent.html', {'user': user})

def verify_otp(request):
    if request.method == 'POST':
        user = request.user
        otp = request.POST.get('otp')

        # Verify the OTP entered by the user.
        device = TOTPDevice.objects.get(user=user)
        is_verified = device.verify_token(otp)

        if is_verified:
            # Mark OTPVerification as verified.
            OTPVerification.objects.filter(user=user).update(is_verified=True)
            return render(request, 'otp_verified.html', {'user': user})

    return render(request, 'otp_verification.html', {'user': user})


def send_page_url_via_email(recipient_email, page_name):
    subject = 'Here is the URL of the page you requested'
    page_url = settings.BASE_URL + reverse(page_name)  
    message = f'Please find the URL of the page: {page_url}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]
    send_mail(subject, message, from_email, recipient_list)


# def home(request):
#     # Your view logic for the home page here...
#     # ...

#     # Assuming the recipient's email is stored in the variable 'recipient_email'
#     recipient_email = 'recipient@example.com'
#     send_page_url_via_email(recipient_email, 'home')

#     return render(request, 'home.html')



@login_required(login_url="/login/")
def leaderboard(request):
    members = Member.objects.all()
    codechef_list = [member.codechef_user for member in members]
    codeforces_list = [member.codeforces_user for member in members]
    return render(request, "leaderboard.html", context = {'page': "LeaderBorad",'codechef_list':codechef_list,'codeforces_list':codeforces_list,'members': members})

