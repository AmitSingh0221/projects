from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import ActivityLog, EmailApproval

def send_approved_email(approval, user):
    if approval.status != EmailApproval.Status.PENDING:
        raise ValueError("Only pending email drafts can be sent.")
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        raise RuntimeError("SMTP credentials are not configured.")
    sent = send_mail(
        subject=approval.subject,
        message=approval.body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[approval.recipient],
        fail_silently=False,
    )
    if sent != 1:
        approval.status = EmailApproval.Status.FAILED
        approval.save(update_fields=["status"])
        ActivityLog.objects.create(inquiry=approval.inquiry, event="email_failed", details="SMTP did not confirm delivery.")
        raise RuntimeError("Email backend did not report a successful send.")
    approval.status = EmailApproval.Status.SENT
    approval.sent_at = timezone.now()
    approval.approved_by = user
    approval.save(update_fields=["status", "sent_at", "approved_by"])
    approval.inquiry.status = approval.inquiry.Status.REPLIED
    approval.inquiry.save(update_fields=["status", "updated_at"])
    ActivityLog.objects.create(inquiry=approval.inquiry, event="email_sent", details=f"Approved email sent to {approval.recipient}.")
