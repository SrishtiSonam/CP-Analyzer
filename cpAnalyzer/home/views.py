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
    first_member_codeforces = "neal : 3019"
    first_member_codechef = "namanlp : 1847"
    first_member_leetcode = "sopheary : 721,305"
    return render(request, "index.html", context={'page':"CP_Tracker",'first_member_codeforces':first_member_codeforces,'first_member_codechef':first_member_codechef,'first_member_leetcode':first_member_leetcode})
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
            leetcode_list = [member.leetcode_user for member in members]
            for member in members:
                member.codeforces_problem = codeforces_problems_solved(member.codeforces_user)
                member.codeforces_rating = codeforces_rating(member.codeforces_user)
                member.codeforces_recent = f"https://codeforces.com/submissions/{member.codeforces_user}"
                member.codechef_problem = codechef_problems_solved(member.codechef_user)
                member.codechef_rating = codechef_rating(member.codechef_user)
                member.codechef_recent = f"https://www.codechef.com/users/{member.codechef_user}"
                member.leetcode_problem = leetcode_total_problems_solved(member.leetcode_user)
                member.leetcode_ranking = leetcode_ranking(member.leetcode_user)
                member.leetcode_recent = f"https://leetcode.com/{member.leetcode_user}"
                member.total_problem = total_problems_solved(member.codeforces_user,member.codechef_user,member.leetcode_user)
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

    otp_secret_key = random_hex(20)
    otp_verification, _ = OTPVerification.objects.update_or_create(
        user=user, defaults={'secret_key': otp_secret_key}
    )

    otp = str(random.randint(100000, 999999))
    print(f"Your OTP: {otp}")

    TOTPDevice.objects.create(user=user, tolerance=1, secret=otp)

    return render(request, 'otp_sent.html', {'user': user})

def verify_otp(request):
    if request.method == 'POST':
        user = request.user
        otp = request.POST.get('otp')

        device = TOTPDevice.objects.get(user=user)
        is_verified = device.verify_token(otp)

        if is_verified:
            OTPVerification.objects.filter(user=user).update(is_verified=True)
            return render(request, 'otp_verified.html', {'user': user})

    return render(request, 'otp_verification.html', {'user': user})


def send_page_url_via_email(recipient_email, page_name, username):
    subject = 'Login Request for CPAnalyzer'
    page_url = settings.BASE_URL + reverse(page_name)  
    message = f'Dear {username},\n I hope this email finds you well. We\'re reaching out from CPAnalyzer in response to your request for login credentials via URL.\n As requested, here is the URL to access your account: {page_url}.\n If you encounter any issues or have any questions, please don\'t hesitate to reach out to our support team. We\'re here to assist you!\n Thank you for choosing CPAnalyzer for your needs. We look forward to serving you.\nBest regards,\n CPAnalyzer Support Team'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]
    send_mail(subject, message, from_email, recipient_list)

def emailPage(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        recipient_email = data.get('recipient_email')
        send_page_url_via_email(recipient_email, 'leaderboard', username)
        messages.success(request, "Email has been sent on your account, please check your gmail inbox.")
    return render(request, "emailPage.html", context = {'page': "Login_Email_Page"})



@login_required(login_url="/login/")
def leaderboard(request):
    members = Member.objects.all()
    codechef_list = [member.codechef_user for member in members]
    codeforces_list = [member.codeforces_user for member in members]
    leetcode_list = [member.leetcode_user for member in members]
    for member in members:
        member.codeforces_problem = codeforces_problems_solved(member.codeforces_user)
        member.codeforces_rating = codeforces_rating(member.codeforces_user)
        member.codeforces_recent = f"https://codeforces.com/submissions/{member.codeforces_user}"
        member.codechef_problem = codechef_problems_solved(member.codechef_user)
        member.codechef_rating = codechef_rating(member.codechef_user)
        member.codechef_recent = f"https://www.codechef.com/users/{member.codechef_user}"
        member.leetcode_problem = leetcode_total_problems_solved(member.leetcode_user)
        member.leetcode_ranking = leetcode_ranking(member.leetcode_user)
        member.leetcode_recent = f"https://leetcode.com/{member.leetcode_user}"
        member.total_problem = total_problems_solved(member.codeforces_user,member.codechef_user,member.leetcode_user)

        # rollNo = member.rollNo
        # name = member.name
        # total_problems = member.total_problem
        # leaderboard.objects.create(
        #     rollNo=rollNo,
        #     name=name,
        #     total_problems=total_problems,
        # )

    sorted_members = sorted(members, key=lambda x: x['total_problem'], reverse=True)
    codeforces_sorted_members = sorted(members, key=lambda x: x['codeforces_problem'], reverse=True)
    codechef_sorted_members = sorted(members, key=lambda x: x['codechef_problem'], reverse=True)
    leetcode_sorted_members = sorted(members, key=lambda x: x['leetcode_problem'], reverse=True)
    
    return render(request, "leaderboard.html", context = {'page': "LeaderBorad",'sorted_members':sorted_members,'codeforces_sorted_members':codeforces_sorted_members, 'codechef_sorted_members':codechef_sorted_members,'leetcode_sorted_members':leetcode_sorted_members})
