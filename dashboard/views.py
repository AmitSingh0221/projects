from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import render
from customers.models import Customer
from leads.models import Lead
from inquiries.models import Inquiry
from automations.models import FollowUp, EmailApproval

@login_required
def dashboard_home(request):
    daily = list(Inquiry.objects.values("created_at__date").annotate(total=Count("id")).order_by("created_at__date")[-7:])
    context = {
        "customer_count": Customer.objects.count(),
        "lead_count": Lead.objects.count(),
        "inquiry_count": Inquiry.objects.count(),
        "high_priority_count": Lead.objects.filter(priority=Lead.Priority.HIGH).count(),
        "pending_approvals": EmailApproval.objects.filter(status=EmailApproval.Status.PENDING).count(),
        "pending_followups": FollowUp.objects.filter(status=FollowUp.Status.PENDING).count(),
        "pipeline_value": Lead.objects.filter(status__in=[Lead.Status.NEW, Lead.Status.CONTACTED, Lead.Status.QUALIFIED]).aggregate(total=Sum("estimated_value"))["total"] or 0,
        "recent_inquiries": Inquiry.objects.select_related("customer")[:8],
        "daily_labels": [str(x["created_at__date"]) for x in daily],
        "daily_values": [x["total"] for x in daily],
    }
    return render(request, "dashboard/home.html", context)
