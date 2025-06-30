from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .forms import RegistrationForm
from .decoratprs import anonymous_required
import json
import random

User = get_user_model()

def send_verification_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')

            if not email:
                return JsonResponse({'success': False, 'message': 'Email is required'}, status=400)

            # Generate and store new code
            code = str(random.randint(100000, 999999))  # Ensure it's always a string
            request.session['verification_code'] = code
            request.session['verification_email'] = email
            
            # Only store registration data if this is initial registration
            if username and password:
                if username.lower() == password.lower():
                    return JsonResponse({
                        'success': False,
                        'message': 'Username and password cannot be similar'
                    }, status=400)

                if User.objects.filter(email=email).exists():
                    return JsonResponse({'success': False, 'message': 'Email already registered'}, status=400)

                request.session['registration_data'] = {
                    'username': username,
                    'email': email,
                    'password': password
                }
            
            # Save the session explicitly
            request.session.modified = True

            send_mail(
                'Your Verification Code',
                f'Your verification code is: {code}',
                'saman.karimian12@gmail.com',
                [email],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': 'Verification code sent'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@ensure_csrf_cookie
@anonymous_required
def register_user(request):
    if request.method == 'GET':
        # Check if coming from verification step
        if 'registration_data' in request.session:
            return redirect('/verify/')
        return render(request, "register/registration.html", {'form': RegistrationForm()})

    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST.dict()

            # Check if username and password are similar
            if data.get('username') and data.get('password1'):
                if data.get('username').lower() == data.get('password1').lower():
                    return JsonResponse({
                        'success': False,
                        'errors': {'password1': 'Username and password cannot be similar'}
                    }, status=400)

            session_email = request.session.get('verification_email')
            if data.get('email') != session_email:
                return JsonResponse({
                    'success': False,
                    'errors': {'email': 'Email does not match verification request'}
                }, status=400)

            # Verify the code
            session_code = request.session.get('verification_code')
            if not session_code or data.get('verification_code') != session_code:
                return JsonResponse({
                    'success': False,
                    'errors': {'verification_code': 'Invalid verification code'}
                }, status=400)

            form = RegistrationForm(data, request=request)

            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()

                authenticated_user = authenticate(
                    request, 
                    username=user.username, 
                    password=form.cleaned_data['password1']
                )
                if authenticated_user is not None:
                    login(request, authenticated_user)
                else:
                    return JsonResponse({
                        'success': False, 
                        'message': 'Authentication failed after registration'
                    }, status=400)

                # Clean up session
                request.session.pop('verification_code', None)
                request.session.pop('verification_email', None)
                request.session.pop('registration_data', None)

                return JsonResponse({
                    'success': True,
                    'redirect_url': '/',
                    'message': 'Registration successful!'
                })
            else:
                errors = {field: error_list[0] for field, error_list in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        
@ensure_csrf_cookie
@anonymous_required
def verification_view(request):
    if request.method == 'GET':
        if 'registration_data' not in request.session or 'verification_code' not in request.session:
            return redirect('/register/')
        
        # Initialize failed attempts counter if it doesn't exist
        if 'verification_attempts' not in request.session:
            request.session['verification_attempts'] = 0
            request.session.modified = True
            
        return render(request, "register/verification.html")
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST.dict()
            
            # Increment attempts counter
            request.session['verification_attempts'] = request.session.get('verification_attempts', 0) + 1
            request.session.modified = True
            
            # Convert both codes to strings for consistent comparison
            session_code = str(request.session.get('verification_code', ''))
            submitted_code = str(data.get('verification_code', ''))
            
            if not session_code or submitted_code != session_code:
                # Check if exceeded max attempts
                if request.session['verification_attempts'] >= 3:
                    return JsonResponse({
                        'success': False,
                        'errors': {'verification_code': 'Invalid verification code'},
                        'exceeded_attempts': True
                    }, status=400)
                
                return JsonResponse({
                    'success': False,
                    'errors': {'verification_code': 'Invalid verification code'}
                }, status=400)

            print("Session code:", session_code)
            print("User submitted:", submitted_code)



            # Get registration data from session
            reg_data = request.session['registration_data']
            form_data = {
                'username': reg_data['username'],
                'email': reg_data['email'],
                'password1': reg_data['password'],
                'password2': reg_data['password'],
                'verification_code': data.get('verification_code')
            }
            
            form = RegistrationForm(form_data, request=request)

            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.set_password(form.cleaned_data['password1'])
                user.save()

                # Authenticate and login
                authenticated_user = authenticate(
                    request,
                    username=user.username,
                    password=form.cleaned_data['password1']
                )
                
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    
                    # Clean up session
                    request.session.pop('verification_code', None)
                    request.session.pop('verification_email', None)
                    request.session.pop('registration_data', None)

                    return JsonResponse({
                        'success': True,
                        'redirect_url': '/',
                        'message': 'Registration successful!'
                    })
                
            errors = {field: error_list[0] for field, error_list in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return redirect('/register/')


@csrf_exempt
def clear_registration_session(request):
    if request.method == 'POST':
        keys = ['verification_code', 'verification_email', 'registration_data']
        for key in keys:
            if key in request.session:
                del request.session[key]
        request.session.modified = True
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)



@csrf_exempt
def clear_registration_session(request):
    if request.method == 'POST':
        keys = ['verification_code', 'verification_email', 'registration_data', 'verification_attempts']
        for key in keys:
            if key in request.session:
                del request.session[key]
        request.session.modified = True
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)




