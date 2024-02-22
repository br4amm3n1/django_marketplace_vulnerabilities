from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile, Transaction
from devices.models import Review
from devices.forms import ReviewSearchForm
from .forms import UserPictureForm, UserBioForm, UserEditForm, TransactionForm, RegistrationForm
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.views.decorators.http import require_GET


@require_GET
def custom_logout_view(request):
    logout(request)
    return redirect('device_showcase')


def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('device_showcase')
        else:
            return render(request, 'accounts/login.html', {'error_message': 'Неверное имя пользователя или пароль'})
    else:
        return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        # user_form = UserCreationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

            profile, created = Profile.objects.get_or_create(user=user)
            profile.save()

            group = Group.objects.get(name='user')
            user.groups.add(group)

            login(request, user)
            return redirect('device_showcase')
    else:
        user_form = RegistrationForm()

    return render(request, 'accounts/register.html', {'user_form': user_form})


@login_required
def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    user_info = request.user
    user_reviews = Review.objects.select_related('device', 'author') \
                                 .only('id', 'device__name', 'content', 'rating',
                                       'author__username', 'author__first_name',
                                       'author__last_name', 'author__email', 'device_id') \
                                 .filter(author=request.user)

    search_form = ReviewSearchForm()
    if request.method == 'GET':
        search_form = ReviewSearchForm(request.GET)
        if search_form.is_valid():
            search_word = search_form.cleaned_data.get('search_word')
            if search_word:
                user_reviews = Review.objects.filter(author=request.user, content__icontains=search_word)

    if request.method == 'POST':
        user_edit_form = UserEditForm(request.POST, instance=request.user)
        user_bio_form = UserBioForm(request.POST, instance=user_profile)

        if user_edit_form.is_valid():
            if user_edit_form.has_changed():
                user_edit_form.save()

        if user_bio_form.is_valid():
            user_bio_form.save()

    else:
        user_edit_form = UserEditForm(instance=request.user)
        user_bio_form = UserBioForm(instance=user_profile)

    return render(request, 'accounts/profile_page.html', {'user_profile': user_profile,
                                                          'user_edit_form': user_edit_form,
                                                          'user_info': user_info,
                                                          'user_bio_form': user_bio_form,
                                                          'user_reviews': user_reviews,
                                                          'search_form': search_form})


@login_required
def upload_profile_picture(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        profile_picture_form = UserPictureForm(request.POST, request.FILES, instance=user_profile)

        if profile_picture_form.is_valid():
            if profile_picture_form.has_changed():
                profile_picture_form.save()
    return redirect('profile')


@login_required
def process_payment(request):
    if request.method == 'POST':
        payment_form = TransactionForm(request.POST)

        if payment_form.is_valid():
            user = request.user
            transaction_data = {**payment_form.cleaned_data, 'user': user}
            Transaction.objects.create(**transaction_data)

            user_profile = Profile.objects.get(user=user)
            user_profile.balance += transaction_data['amount']
            user_profile.save()

            return redirect('profile')

    else:
        payment_form = TransactionForm()

    return render(request, 'accounts/payment_page.html', {'payment_form': payment_form})
