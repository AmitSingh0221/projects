from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import strip_tags
from customers.models import Customer
from leads.models import Lead
from ai_engine.services import analyze_inquiry
from automations.models import ActivityLog, EmailApproval
from automations.services import send_approved_email
from .forms import PublicInquiryForm, InquiryCreateForm
from .models import Inquiry

def public_inquiry(request):
    form = PublicInquiryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        customer, _ = Customer.objects.get_or_create(
            email=data["email"].lower(),
            defaults={"name": data["name"], "company": data.get("company", "")},
        )
        inquiry = Inquiry.objects.create(customer=customer, subject=data["subject"], message=data["message"])
        try:
            result = analyze_inquiry(inquiry.message)
            inquiry.ai_intent = result["intent"][:100]
            inquiry.ai_summary = result["summary"]
            inquiry.ai_response = result["response"]
            inquiry.status = Inquiry.Status.NEEDS_REVIEW
            inquiry.requires_approval = True
            priority = result["priority"].lower()
            lead, _ = Lead.objects.get_or_create(
                customer=customer, title=inquiry.subject,
                defaults={"description": inquiry.ai_summary, "priority": priority, "source": "website"},
            )
            inquiry.lead = lead
            inquiry.save()
            ActivityLog.objects.create(inquiry=inquiry, event="ai_analysis", details="Inquiry analyzed and reply drafted; approval required.")
            EmailApproval.objects.create(inquiry=inquiry, recipient=customer.email, subject=f"Re: {inquiry.subject}", body=inquiry.ai_response)
            messages.success(request, "Inquiry received. An AI-assisted draft was created for business review.")
        except Exception as exc:
            inquiry.status = Inquiry.Status.RECEIVED
            inquiry.save(update_fields=["status", "updated_at"])
            ActivityLog.objects.create(inquiry=inquiry, event="ai_error", details=f"AI processing failed: {type(exc).__name__}")
            messages.warning(request, "Inquiry saved, but AI analysis was unavailable. The business team can review it.")
        return redirect("public_inquiry")
    return render(request, "inquiries/public_form.html", {"form": form})

@login_required
def inquiry_list(request):
    inquiries = Inquiry.objects.select_related("customer", "lead")
    return render(request, "inquiries/list.html", {"inquiries": inquiries})

@login_required
def inquiry_create(request):
    form = InquiryCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        inquiry = form.save()
        try:
            result = analyze_inquiry(inquiry.message)
            inquiry.ai_intent = result["intent"][:100]
            inquiry.ai_summary = result["summary"]
            inquiry.ai_response = result["response"]
            inquiry.status = Inquiry.Status.NEEDS_REVIEW
            inquiry.save()
            lead, _ = Lead.objects.get_or_create(
                customer=inquiry.customer, title=inquiry.subject,
                defaults={"description": inquiry.ai_summary, "priority": result["priority"].lower(), "source": "manual"},
            )
            inquiry.lead = lead
            inquiry.save(update_fields=["lead", "updated_at"])
            EmailApproval.objects.create(inquiry=inquiry, recipient=inquiry.customer.email, subject=f"Re: {inquiry.subject}", body=inquiry.ai_response)
            ActivityLog.objects.create(inquiry=inquiry, event="ai_analysis", details="Draft created; approval required.")
            messages.success(request, "Inquiry analyzed. Review the draft before sending.")
        except Exception:
            messages.warning(request, "Inquiry saved, but AI analysis failed. Check the API key and logs.")
        return redirect("inquiry_list")
    return render(request, "form.html", {"form": form, "title": "Create inquiry"})

@login_required
def inquiry_detail(request, pk):
    inquiry = get_object_or_404(Inquiry.objects.select_related("customer", "lead"), pk=pk)
    approvals = EmailApproval.objects.filter(inquiry=inquiry).order_by("-created_at")
    logs = ActivityLog.objects.filter(inquiry=inquiry).order_by("-created_at")
    return render(request, "inquiries/detail.html", {"inquiry": inquiry, "approvals": approvals, "logs": logs})

@login_required
def approve_email(request, approval_id):
    from django.views.decorators.http import require_POST
    approval = get_object_or_404(EmailApproval.objects.select_related("inquiry"), pk=approval_id)
    if request.method != "POST":
        return redirect("inquiry_detail", pk=approval.inquiry_id)
    if approval.status != EmailApproval.Status.PENDING:
        messages.warning(request, "This approval is no longer pending.")
        return redirect("inquiry_detail", pk=approval.inquiry_id)
    try:
        send_approved_email(approval, request.user)
        messages.success(request, "Email sent.")
    except Exception:
        messages.error(request, "Email could not be sent. Check SMTP configuration and the activity log.")
    return redirect("inquiry_detail", pk=approval.inquiry_id)
