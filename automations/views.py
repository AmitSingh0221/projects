from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from inquiries.models import Inquiry
from .models import FollowUp, ActivityLog

@login_required
def followup_list(request):
    if request.method == "POST":
        inquiry_id = request.POST.get("inquiry_id")
        inquiry = Inquiry.objects.filter(pk=inquiry_id).first()
        if inquiry:
            FollowUp.objects.create(inquiry=inquiry, due_at=timezone.now() + timedelta(days=3))
            ActivityLog.objects.create(inquiry=inquiry, event="followup_scheduled", details="Follow-up scheduled for three days from now.")
            messages.success(request, "Follow-up scheduled for three days from now.")
        else:
            messages.error(request, "Select a valid inquiry.")
        return redirect("followup_list")
    return render(request, "automations/followups.html", {
        "followups": FollowUp.objects.select_related("inquiry", "inquiry__customer").order_by("due_at"),
        "inquiries": Inquiry.objects.exclude(status__in=[Inquiry.Status.REPLIED, Inquiry.Status.CLOSED]),
    })
