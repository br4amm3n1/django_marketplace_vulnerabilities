from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import Profile
# from accounts.forms import RegistrationForm
from django.contrib.auth.models import Group


class TestProfileViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_upload_profile_picture_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('upload_profile_picture'), {'profile_picture': 'usb-накопитель_LjC1Srh.jpg'})
        self.assertEqual(response.status_code, 302)

    def test_process_payment_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('process_payment'), {'card_number': '1234567812345678',
                                                                 'expiry_date': '12/23', 'cvc': '123',
                                                                 'card_holder': 'John Doe', 'amount': '50.00'})
        self.assertEqual(response.status_code, 302)


class TestCustomLoginViews(TestCase):
    def test_login_success(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        profile = Profile.objects.create(user=user)
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('device_showcase'))

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {'username': 'nonexistentuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)


class TestRegisterViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = '/accounts/register/'
        self.group = Group.objects.create(name='user')

    def test_registration_success(self):
        data = {
            'username': 'testuser',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        }

        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.assertTrue(User.objects.filter(username='testuser').exists())

        user = User.objects.get(username='testuser')
        self.assertTrue(Profile.objects.filter(user=user).exists())

        user = User.objects.get(username='testuser')
        user.groups.add(self.group)
        self.assertTrue(user.groups.filter(name='user').exists())

        self.assertTrue(user.is_authenticated)

    def test_registration_form_validation(self):
        invalid_data = {
            'username': '',
            'password1': 'w',
            'password2': 'differentpassword',
        }

        response = self.client.post(self.register_url, invalid_data)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'This field is required.')

        self.assertFalse(User.objects.filter(username='').exists())
