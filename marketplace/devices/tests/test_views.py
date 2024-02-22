from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from devices.models import Device, Category
from accounts.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile


class TestDeviceViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        image_file = SimpleUploadedFile("acernitro.png", content=b"file_content", content_type="image/png")
        self.category = Category.objects.create(name='Test Category')
        self.device = Device.objects.create(name='TestDevice', category=self.category, image=image_file)
        self.profile = Profile.objects.create(user=self.user)
        self.review_data = {'rating': 5, 'content': 'Great device!'}
        self.review_form_data = {'rating': 4, 'content': 'Good device!'}

    def test_device_showcase_view(self):
        url = reverse('device_showcase')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'devices/device_showcase.html')

    def test_device_detail_view(self):
        url = reverse('device_detail', kwargs={'device_id': self.device.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'devices/device_detail.html')
        self.assertContains(response, 'TestDevice')

    def test_show_device_by_category_view(self):
        url = reverse('devices_by_category', kwargs={'category_id': self.category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'devices/devices_by_category.html')
        self.assertContains(response, self.device.name)

    def test_show_device_categories_view(self):
        url = reverse('device_categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'devices/device_categories.html')
        self.assertContains(response, 'Test Category')

    def test_create_review_view(self):
        url = reverse('create_review', kwargs={'device_id': self.device.id})
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(url, data=self.review_form_data)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'devices/device_detail.html')
        self.assertIn('review_form', response.context)

    def test_show_device_reviews_view(self):
        url = reverse('device_reviews', kwargs={'device_id': self.device.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'devices/device_reviews.html')
