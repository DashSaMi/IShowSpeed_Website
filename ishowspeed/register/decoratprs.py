from django.shortcuts import redirect
from functools import wraps
from django.http import JsonResponse, HttpResponse

def anonymous_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'redirect': True,
                    'message': 'You are already registered and logged in',
                    'redirect_url': '/'
                }, status=403)
            return redirect('main_page')
        
        # Ensure the view returns a proper response
        response = view_func(request, *args, **kwargs)
        if response is None:
            return HttpResponse(status=204)  # Return empty response if needed
        return response
    return _wrapped_view