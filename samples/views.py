from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Sample
from .forms import SampleForm
# Create your views here.


@staff_member_required(login_url="login")
def index(request):
    query = request.GET.get('q')
    page_number = request.GET.get('page')
    if query:
        samples = Sample.objects.filter(number__icontains=query).order_by('-id')
        if not samples:
            samples = Sample.objects.filter(customer__name__icontains=query).order_by('-id')
        if not samples:
            samples = Sample.objects.filter(product__name__icontains=query).order_by('-id')
    else:
        samples = Sample.objects.all().order_by('-id')
    paginator = Paginator(samples, 10)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, "samples/index.html", context)


@staff_member_required(login_url="login")
def add_sample(request):
    form = SampleForm(request.POST or None)
    if form.is_valid():
        number = form.cleaned_data['number']
        receipt_date = form.cleaned_data['receipt_date']
        customer = form.cleaned_data['customer']
        product = form.cleaned_data['product']
        sampling_date = form.cleaned_data['sampling_date']
        sampling_point = form.cleaned_data['sampling_point']
        last_sample = Sample.objects.last()
        sample = Sample()
        sample.number = last_sample.number + 1
        sample.receipt_date = receipt_date
        sample.customer = customer
        sample.product = product
        sample.sampling_date = sampling_date
        sample.sampling_point = sampling_point
        try:
            sample.save()
            msg = f"<b>{sample}</b> was added successfully."
            messages.add_message(request, messages.SUCCESS, msg)
            return redirect("samples:index")
        except ValueError:
            msg = f"Couldn't add <b>{sample}</b>. Please try again later."
            messages.add_message(request, messages.ERROR, msg)
    context = {
        'form': form,
    }
    return render(request, "samples/add_sample.html", context)


@staff_member_required(login_url="login")
def sample_details(request, sample_id):
    form = SampleForm(request.POST or None)
    if form.is_valid():
        number = form.cleaned_data['number']
        receipt_date = form.cleaned_data['receipt_date']
        customer = form.cleaned_data['customer']
        product = form.cleaned_data['product']
        sampling_date = form.cleaned_data['sampling_date']
        sampling_point = form.cleaned_data['sampling_point']
        report_date = form.cleaned_data['report_date']
        sample = Sample.objects.get(pk=sample_id)
        sample.number = number
        sample.receipt_date = receipt_date
        sample.customer = customer
        sample.product = product
        sample.sampling_date = sampling_date
        sample.sampling_point = sampling_point
        sample.report_date = report_date
        try:
            sample.save()
            msg = f"<b>{sample}</b> was updated successfully."
            messages.add_message(request, messages.SUCCESS, msg)
        except ValueError:
            msg = f"Couldn't update <b>{sample}</b>. Please try again later."
            messages.add_message(request, messages.ERROR, msg)
    else:
        if request.method == "GET":
            sample = Sample.objects.get(pk=sample_id)
            form = SampleForm(instance=sample)
    context = {
        'form': form,
    }
    return render(request, "samples/details.html", context)
