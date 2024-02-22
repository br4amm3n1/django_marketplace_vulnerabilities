from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import Profile
from django.contrib.auth.models import Group
from devices.models import Category, Device, Review
from control_panel.logic import remove_review, create_category, remove_category, add_device


class TestControlPanelViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)

        self.moderator_user = User.objects.create_user(username='moderator', password='moderatorpassword')
        self.moderator_profile = Profile.objects.create(user=self.moderator_user)
        self.moderator_group = Group.objects.create(name='moderator')
        self.moderator_user.groups.add(self.moderator_group)
        self.moderator_profile.save()

    def test_view_capabilities(self):
        client = Client()

        response = client.get('/control_panel/')
        self.assertEqual(response.status_code, 302)

        client.login(username="testuser", password="testpassword")
        response = client.get('/control_panel/')
        self.assertEqual(response.status_code, 403)
        client.logout()

        client.login(username='moderator', password='moderatorpassword')
        response = client.get('/control_panel/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'control_panel/main_page.html')

    def test_view_reviews(self):
        client = Client()
        client.login(username='moderator', password='moderatorpassword')

        response = client.get('/control_panel/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'control_panel/list_reviews.html')

    def test_view_purchases(self):
        client = Client()
        client.login(username='moderator', password='moderatorpassword')

        response = client.get('/control_panel/purchases/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'control_panel/list_purchases.html')

    def test_view_transactions(self):
        client = Client()
        client.login(username='moderator', password='moderatorpassword')

        response = client.get('/control_panel/transactions/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'control_panel/list_transactions.html')

    def test_create_category(self):
        client = Client()
        client.login(username='moderator', password='moderatorpassword')

        response = self.client.post(reverse('view_capabilities'), {'create_category': True, 'name': 'TestCategory'})
        create_category(response.wsgi_request)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name="TestCategory").exists())

    def test_remove_category(self):
        client = Client()
        client.login(username='moderator', password='moderatorpassword')

        category = Category.objects.create(name='TestCategory')
        response = self.client.post(reverse('view_capabilities'), {'remove_category': True, 'name': 'TestCategory'})
        remove_category(response.wsgi_request)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Category.objects.filter(name=category.id).exists())

    def test_remove_review(self):
        client = Client()
        client.login(username='moderator', password='moderatorpassword')

        review = Review.objects.create(
            content='Test review content',
            rating=5,
            author=self.user,
            device=Device.objects.create(name='TestDevice')
        )

        response = self.client.post(reverse('view_reviews'), {'delete_review_id': review.id})
        remove_review(response.wsgi_request)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_add_device(self):
        client = Client()
        client.login(username='moderator', password='moderatorpassword')

        category = Category.objects.create(name='TestCategory')

        form_data = {
            'name': 'TestDevice',
            'description': 'TestDescription',
            'price': '100.00',
            'category': category.id,
        }

        response = client.post('/control_panel/', form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(Device.objects.filter(name='TestDevice').exists())
