from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import FollowUp, ActivityLog

@shared_task
def process_due_followups():
    due = FollowUp.objects.select_related("inquiry", "inquiry__customer").filter(
        status=FollowUp.Status.PENDING, due_at__lte=timezone.now()
    )[:100]
    processed = 0
    for item in due:
        inquiry = item.inquiry
        # Do not follow up if the customer has already received a reply.
        if inquiry.status in {inquiry.Status.REPLIED, inquiry.Status.CLOSED}:
            item.status = FollowUp.Status.CANCELLED
            item.save(update_fields=["status"])
            continue
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            continue
        try:
            send_mail(
                subject=f"Following up: {inquiry.subject}",
                message=f"Hello {inquiry.customer.name},\n\nWe are following up on your inquiry: {inquiry.subject}. Please let us know if we can help.\n",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[inquiry.customer.email],
                fail_silently=False,
            )
            item.status = FollowUp.Status.SENT
            item.sent_at = timezone.now()
            item.save(update_fields=["status", "sent_at"])
            ActivityLog.objects.create(inquiry=inquiry, event="followup_sent", details=f"Follow-up sent to {inquiry.customer.email}.")
            processed += 1
        except Exception as exc:
            ActivityLog.objects.create(inquiry=inquiry, event="followup_failed", details=type(exc).__name__)
    return processed
