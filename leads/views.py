from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import LeadForm
from .models import Lead

@login_required
def lead_list(request):
    leads = Lead.objects.select_related("customer")
    status = request.GET.get("status", "")
    if status:
        leads = leads.filter(status=status)
    return render(request, "leads/list.html", {"leads": leads, "status": status, "statuses": Lead.Status.choices})

@login_required
def lead_create(request):
    form = LeadForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Lead created.")
        return redirect("lead_list")
    return render(request, "form.html", {"form": form, "title": "Add lead"})

@login_required
def lead_update(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    form = LeadForm(request.POST or None, instance=lead)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Lead updated.")
        return redirect("lead_list")
    return render(request, "form.html", {"form": form, "title": "Edit lead"})

@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == "POST":
        lead.delete()
        messages.success(request, "Lead deleted.")
        return redirect("lead_list")
    return render(request, "confirm_delete.html", {"object": lead, "cancel_url": "lead_list"})
