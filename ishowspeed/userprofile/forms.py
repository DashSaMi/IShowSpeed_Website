from django import forms
from register.models import CustomUser

class ProfileUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        help_text="Leave blank to keep your current password.",
        label="New Password"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'member_type', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap class for all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # Optional: prefill password field as empty (don't show hashed value)
        self.fields['password'].initial = ''

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 9:
            raise forms.ValidationError("Password must be at least 9 characters long.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)  # update password securely
        else:
            # Do NOT change the password if the field was left empty
            user.password = CustomUser.objects.get(pk=user.pk).password

        if commit:
            user.save()
        return user
    
from django import forms

class ProfileDisplayForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'readonly': 'true'  # Disable input
        }),
        label='Username'
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'readonly': 'true'  # Disable input
        }),
        label='Email'
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'placeholder': 'Enter new password on EditProfile page',
           'readonly': 'true'  # Disable input
        }),
        label='Password'
    )

    member_type = forms.ChoiceField(
        choices=[
        ('old_viewer', 'Old Viewer'),
        ('subscriber', 'Subscriber'),
        ('fan', 'Fan'),
        ('lover', 'Lover'),
        ('cr7_fan', 'CR7 Fan'),
        ('legend', 'Legend'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'member_type',
            'disabled': 'true'  # Correct way to disable <select>
        }),
        label='Member Type'
    )

