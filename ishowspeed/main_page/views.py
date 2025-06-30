from django.shortcuts import render, redirect
from register.models import CustomUser  # Import your CustomUser model

def main_page(request):
    user_count = CustomUser.objects.count()
    user_count+=1000
    context = {
        'user_count': user_count,
    }
    return render(request, "main_page/index.html", context)
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('main_page')  # Assuming 'main_page' is the name of your main page URL