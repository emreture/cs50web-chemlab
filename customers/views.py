from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.html import escape
from .models import Customer
from .forms import CustomerForm

# Create your views here.


@staff_member_required(login_url="login")
def index(request):
    goto_last_page = False
    query = request.GET.get('q')
    page_number = request.GET.get('page')
    form = CustomerForm(request.POST or None)

    if form.is_valid():
        name = form.cleaned_data['name']
        address = form.cleaned_data['address']
        customer = Customer(name=name, address=address)
        try:
            customer.save()
            # raise ValueError
            escaped_customer_name = escape(customer.name)
            msg = f"<b>{escaped_customer_name}</b> was saved successfully."
            messages.add_message(request, messages.SUCCESS, msg)
            query = None
            goto_last_page = True
            form = CustomerForm()
        except ValueError:
            escaped_customer_name = escape(customer.name)
            msg = f"Couldn't save <b>{escaped_customer_name}</b>. Please try again later."
            messages.add_message(request, messages.ERROR, msg)

    if query:
        customers = Customer.objects.filter(name__icontains=query).order_by('id')
    else:
        customers = Customer.objects.all().order_by('id')
    paginator = Paginator(customers, 5)
    if goto_last_page:
        page_number = paginator.num_pages
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, "customers/index.html", context)


@staff_member_required(login_url="login")
def customer_details(request, customer_id):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        address = form.cleaned_data['address']
        customer = Customer.objects.get(pk=customer_id)
        customer.name = name
        customer.address = address
        try:
            customer.save()
            escaped_customer_name = escape(customer.name)
            msg = f"<b>{escaped_customer_name}</b> was updated successfully."
            messages.add_message(request, messages.SUCCESS, msg)
            return redirect("customers:index")
        except ValueError:
            escaped_customer_name = escape(customer.name)
            msg = f"Couldn't update <b>{escaped_customer_name}</b>. Please try again later."
            messages.add_message(request, messages.ERROR, msg)
    else:
        if request.method == "GET":
            customer = Customer.objects.get(pk=customer_id)
            form = CustomerForm(instance=customer)
    context = {
        'form': form,
    }
    return render(request, "customers/details.html", context)
