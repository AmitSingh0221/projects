from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Customer

class CustomerPageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="tester", password="Strong-test-password-123")
        self.client.force_login(self.user)

    def test_customer_list_loads(self):
        response = self.client.get(reverse("customer_list"))
        self.assertEqual(response.status_code, 200)

    def test_customer_creation(self):
        response = self.client.post(reverse("customer_create"), {
            "name": "A Test", "email": "a@example.com", "phone": "", "company": ""
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Customer.objects.filter(email="a@example.com").exists())
