from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from customers.models import Customer
from .models import Lead

class LeadPageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="tester", password="Strong-test-password-123")
        self.client.force_login(self.user)
        self.customer = Customer.objects.create(name="A Test", email="a@example.com")

    def test_lead_list_loads(self):
        response = self.client.get(reverse("lead_list"))
        self.assertEqual(response.status_code, 200)

    def test_lead_creation(self):
        response = self.client.post(reverse("lead_create"), {
            "customer": self.customer.pk, "title": "New project", "description": "",
            "status": "new", "priority": "medium", "source": "website", "estimated_value": "0"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Lead.objects.filter(title="New project").exists())
