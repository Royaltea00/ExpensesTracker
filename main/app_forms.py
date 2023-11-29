from django import forms
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
# from django.contrib.auth.models import User

from .models import Expense, Category, UserProfile


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'avatar']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False  # Make avatar field not required

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar', False)
        if avatar:
            if avatar.size > 2 * 1024 * 1024:  # 2 MB
                raise forms.ValidationError("File size must be no more than 2 MB.")
            return avatar
        else:
            raise forms.ValidationError("Couldn't read the uploaded image.")


class ChangePasswordForm(SetPasswordForm):
    def __init__(self, *args, user=None, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.user = user
