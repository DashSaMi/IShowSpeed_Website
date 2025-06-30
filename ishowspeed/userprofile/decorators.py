from django.shortcuts import redirect
from django.contrib import messages

def auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You need to be logged in to access this page.")
            return redirect('reg')  # Change 'login' to your login URL name
        return view_func(request, *args, **kwargs)
    return wrapper