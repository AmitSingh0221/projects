from datetime import timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from customers.models import Customer
from leads.models import Lead
from inquiries.models import Inquiry
from .models import FollowUp

class FollowUpModelTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Test Customer", email="test@example.com")
        self.inquiry = Inquiry.objects.create(customer=self.customer, subject="Test", message="A test inquiry message.")

    def test_followup_defaults_to_pending(self):
        item = FollowUp.objects.create(inquiry=self.inquiry, due_at=timezone.now() + timedelta(days=3))
        self.assertEqual(item.status, FollowUp.Status.PENDING)

class DashboardAccessTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
