import random

from django.conf import settings
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserOTP


def login(request):
    if request.user.is_authenticated:
        return redirect('/todo/')
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            get_usr = request.POST.get('user')
            user = User.objects.get(username=get_usr)
            if int(get_otp) == UserOTP.objects.filter(user=user).last().otp:
                user.is_active = True
                user.save()
                auth.login(request, user)
                return redirect('/todo/')
            else:
                messages.error(request, f'You Entered a Wrong OTP')
                return render(request, 'login.html', {'otp': True, 'user': user})

        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/todo/')
        elif not User.objects.filter(username=username).exists():
            messages.error(request,
                             f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('/')
        elif not User.objects.get(username=username).is_active:
            user = User.objects.get(username=username)
            user_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=user, otp=user_otp)
            message = f"Hello {user.username},\nYour OTP is {user_otp}\nThanks!"
            send_mail(
                "Verify Your Email",
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            return render(request, 'login.html', {'otp': True, 'user': user})
        else:
            messages.error(request,
                             f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('/')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('user')
            user = User.objects.get(username=get_user)
            if int(get_otp) == UserOTP.objects.filter(user=user).last().otp:
                user.is_active = True
                user.save()
                return redirect('/')
            else:
                messages.error(request, f'You Entered a Wrong OTP')
                return render(request, 'register.html', {'otp': True, 'user': user})
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['confirm_password']
        is_active = False
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name, is_active=is_active)
                user.save()
                otp = random.randint(100000, 999999)
                UserOTP.objects.create(user=user, otp=otp)

                message = f"Hello {user.username},\nYour OTP is {otp}\nThanks!"

                send_mail(
                    "Verify Your Email",
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
                return render(request, 'register.html', {'otp': True, 'user': user})
        else:
            messages.error(request, 'Password not matching')
            return redirect('register')
    return render(request, 'register.html')


def resend_otp(request):
    if request.method == "GET":
        get_usr = request.GET['user']
        if User.objects.filter(username=get_usr).exists() and not User.objects.get(username=get_usr).is_active:
            user = User.objects.get(username=get_usr)
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=user, otp=usr_otp)
            message = f"Hello {user.username},\nYour OTP is {usr_otp}\nThanks!"
            send_mail(
                "Verify Your Email",
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            return HttpResponse("Resend")
    return HttpResponse("Can't Send ")


def logout(request):
    auth.logout(request)
    return redirect('/')
