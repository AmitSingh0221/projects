from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CustomerForm
from .models import Customer

@login_required
def customer_list(request):
    q = request.GET.get("q", "").strip()
    customers = Customer.objects.all()
    if q:
        from django.db.models import Q
        customers = customers.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(company__icontains=q))
    return render(request, "customers/list.html", {"customers": customers, "q": q})

@login_required
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Customer created.")
        return redirect("customer_list")
    return render(request, "form.html", {"form": form, "title": "Add customer"})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Customer updated.")
        return redirect("customer_list")
    return render(request, "form.html", {"form": form, "title": "Edit customer"})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        messages.success(request, "Customer deleted.")
        return redirect("customer_list")
    return render(request, "confirm_delete.html", {"object": customer, "cancel_url": "customer_list"})
