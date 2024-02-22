from django import forms
from .models import Profile, Transaction
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class RegistrationForm(UserCreationForm):
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserPictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']


class UserBioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['card_number', 'expiry_date', 'cvc', 'card_holder', 'amount']

    card_number = forms.CharField(
        label='Номер карты',
        max_length=16,
        required=True
    )
    expiry_date = forms.CharField(
        label='Срок действия',
        max_length=5, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY'})
    )

    cvc = forms.CharField(
        label='CVC код',
        max_length=3,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '732'})
    )

    card_holder = forms.CharField(
        label='Держатель карты',
        max_length=100,
        required=True
    )

    amount = forms.DecimalField(
        label='Сумма платежа',
        max_digits=10,
        decimal_places=2,
        required=True
    )
