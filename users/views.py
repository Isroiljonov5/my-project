from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile

# Create your views here.
def register(request):
    fname = request.POST.get('firstname')
    lname = request.POST.get('lastname')
    email = request.POST.get('email')
    pasw1 = request.POST.get('password')
    pasw2 = request.POST.get('password_confirm')
    if request.method == 'POST':
        if pasw1 != pasw2:
            messages.error(request, 'Parollar bir xil emas')
            return render(request, 'registration/register.html')
        else:
            if User.objects.filter(username=email).exists():
                messages.error(request, f'{email} ushbu emailda foydalanuvchi mavjud !')
                return render(request, 'registration/register.html')
            else:
                user = User.objects.create_user(email, email, pasw1)
                user.username = email
                user.first_name = fname
                user.last_name = lname
                user.save()
                Profile.objects.create(user=user)

                messages.success(request, 'Ro‘yxatdan muvaffaqiyatli o‘tdingiz !')
                return render(request, 'registration/login.html')
    return render(request, 'registration/register.html')


@login_required
def profile(request):
    return render(request, 'profile/my-profile.html')

def edit_profile(request, username):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        if old_password and new_password1 and new_password2:
            if request.user.check_password(old_password):
                if new_password1 == new_password2:
                    request.user.set_password(new_password1)
                    request.user.save()
                    messages.success(request,'Parol muvaffaqiyatli yangilandi !')
                    return redirect(reverse('users:edit_profile', kwargs={'username':request.user.username}))
                else:
                    messages.error(request, 'Parol bi xil emas')
                    return redirect(reverse('users:edit_profile', kwargs={'username':request.user.username}))
            else:
                messages.error(request, 'Parol notogri !')
                return redirect(reverse('users:edit_profile', kwargs={'username':request.user.username}))
        
        user = User.objects.get(username=username)
        fname = request.POST.get('first_name')
        if fname:
            user.first_name=fname
            user.save()
        lname = request.POST.get('last_nmea')
        if lname:
            user.last_name = lname
            user.save()
        username = request.POST.get('username')
        if username:
            user.username = username
            user.save()
        email = request.POST.get('email')
        if email:
            user.email = email
            user.save()
        image = request.FILES.get('image')
        if image:
            user.profile.image = image
            user.profile.save()
            user.save()
        bio = request.POST.get('bio')
        if bio:
            user.profile.bio = bio
            user.profile.save()
        phone = request.POST.get('phone')
        if phone:
            user.profile.phone = phone
            user.profile.save()
        return render(request , 'profile/my-profile.html')
    return render(request, 'profile/edit-profile.html')