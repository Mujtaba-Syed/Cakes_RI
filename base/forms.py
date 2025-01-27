from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile,User

class SignUpForm(UserCreationForm):
    fullname = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=70, required=True)
    phone_number = forms.CharField()
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2023)))
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES)

    class Meta:
        model = User
        fields = ['fullname', 'username', 'email', 'phone_number', 'date_of_birth', 'password1', 'password2', 'user_type', 'gender']
