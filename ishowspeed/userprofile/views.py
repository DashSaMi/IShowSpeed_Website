from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from register.models import CustomUser
from .forms import ProfileUpdateForm
from django.shortcuts import render
from .decorators import auth_required
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileDisplayForm
from register.models import CustomUser,UserComment
from django.http import JsonResponse


@method_decorator(auth_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm  # Should include username, member_type, and password
    template_name = 'userprofile/edit_profile.html'
    success_url = reverse_lazy('profile_page')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.request.user)  # Keep user logged in if password changed
        messages.success(self.request, 'Profile updated successfully!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_section'] = True
        return context


@auth_required
def profile_page(request):
    user = request.user
    form = ProfileDisplayForm(initial={
        'username': user.username,
        'email': user.email,
        'member_type': user.member_type,
    })
    
    # Get user's comment if it exists
    try:
        user_comment = UserComment.objects.get(commenter=user, user=user)
    except UserComment.DoesNotExist:
        user_comment = None
    
    return render(request, 'userprofile/profile.html', {
        'form': form,
        'user_comment': user_comment
    })



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log out before deleting
        user.delete()
        return redirect('main_page')  # Replace with your homepage URL name
    return redirect('profile')  # Fallback in case accessed via GET


from django.utils import timezone
from datetime import timedelta

@login_required
def post_comment(request, user_pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        comment_text = request.POST.get('comment', '').strip()
        
        # Check if user already has a comment
        try:
            existing_comment = UserComment.objects.get(commenter=request.user, user_id=user_pk)
            
            if not existing_comment.can_edit():
                days_left = existing_comment.days_until_next_edit()
                return JsonResponse({
                    'success': False,
                    'error': f'You can edit your comment again in {days_left} days'
                })
            
            # Update existing comment
            existing_comment.comment = comment_text
            existing_comment.save()
            
            return JsonResponse({
                'success': True,
                'comment': existing_comment.comment,
                'updated_at': existing_comment.updated_at.strftime("%b %d, %Y %I:%M %p")
            })
            
        except UserComment.DoesNotExist:
            # Create new comment if none exists
            if comment_text:
                user_to_comment_on = CustomUser.objects.get(pk=user_pk)
                comment = UserComment.objects.create(
                    user=user_to_comment_on,
                    comment=comment_text,
                    commenter=request.user
                )
                return JsonResponse({
                    'success': True,
                    'comment': comment.comment,
                    'created_at': comment.created_at.strftime("%b %d, %Y %I:%M %p")
                })
            return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})