from django.urls import path
from .views import profile_page, ProfileUpdateView,delete_account,post_comment

urlpatterns = [
     path('', profile_page, name='profile_page'),
     path('edit/<int:pk>/', ProfileUpdateView.as_view(), name='edit_profile'),
     path('delete-account/', delete_account, name='delete_account'),
     path('post-comment/<int:user_pk>/', post_comment, name='post_comment'),
]