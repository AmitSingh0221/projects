from django.db import models
from customers.models import Customer
from leads.models import Lead

class Inquiry(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "received", "Received"
        ANALYZED = "analyzed", "Analyzed"
        NEEDS_REVIEW = "needs_review", "Needs approval"
        REPLIED = "replied", "Replied"
        CLOSED = "closed", "Closed"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="inquiries")
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name="inquiries")
    subject = models.CharField(max_length=200)
    message = models.TextField()
    ai_intent = models.CharField(max_length=100, blank=True)
    ai_summary = models.TextField(blank=True)
    ai_response = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RECEIVED)
    requires_approval = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} — {self.customer.name}"
    class Meta:
        ordering = ["-created_at"]
