from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('member_type', 'legend')
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    MEMBER_CHOICES = [
        ('old_viewer', 'Old Viewer'),
        ('subscriber', 'Subscriber'),
        ('fan', 'Fan'),
        ('lover', 'Lover'),
        ('cr7_fan', 'CR7 Fan'),
        ('legend', 'Legend'),
    ]

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[MinLengthValidator(7, "Username must be at least 7 characters long.")]
    )
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    member_type = models.CharField(
        max_length=20,
        choices=MEMBER_CHOICES,
        default='fan'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        from django.db import transaction
        with transaction.atomic():
            # Handle related objects deletion
            super().delete(*args, **kwargs)
            
from django.utils import timezone
from datetime import timedelta

class UserComment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Track last edit time
    commenter = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name='comments_made')

    def can_edit(self):
        """Check if 5 days have passed since last update"""
        return timezone.now() >= self.updated_at + timedelta(days=5)
    
    def days_until_next_edit(self):
        """Calculate remaining days until next edit is allowed"""
        next_edit_time = self.updated_at + timedelta(days=5)
        remaining = next_edit_time - timezone.now()
        return max(0, remaining.days) + 1  # Ensure positive number and count partial day as fu

    def __str__(self):
        return f"Comment on {self.user.username}'s profile"