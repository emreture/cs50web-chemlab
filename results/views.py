from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import Http404
from django.utils.dateparse import parse_datetime
from samples.models import Sample, Result, TestMethod
from datetime import datetime

# Create your views here.


@login_required(login_url="login")
def index(request):
    query = request.GET.get('q')
    page_number = request.GET.get('page')
    user = request.user
    organization = user.organization.all()
    if query:
        if user.is_staff:
            samples = Sample.objects.filter(number__icontains=query).order_by('-id')
        else:
            samples = Sample.objects.filter(customer__name__in=list(organization)).filter(number__icontains=query).order_by('-id')
        if not samples:
            if user.is_staff:
                samples = Sample.objects.filter(customer__name__icontains=query).order_by('-id')
            else:
                samples = Sample.objects.filter(customer__name__in=list(organization)).filter(customer__name__icontains=query).order_by('-id')
        if not samples:
            if user.is_staff:
                samples = Sample.objects.filter(product__name__icontains=query).order_by('-id')
            else:
                samples = Sample.objects.filter(customer__name__in=list(organization)).filter(product__name__icontains=query).order_by('-id')
        if not samples:
            if user.is_staff:
                samples = Sample.objects.filter(sampling_point__icontains=query).order_by('-id')
            else:
                samples = Sample.objects.filter(customer__name__in=list(organization)).filter(sampling_point__icontains=query).order_by('-id')
    else:
        if user.is_staff:
            samples = Sample.objects.all().order_by('-id')
        else:
            samples = Sample.objects.filter(customer__name__in=list(organization)).order_by('-id')
    paginator = Paginator(samples, 10)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'query': query
    }
    return render(request, "results/index.html", context)


@login_required(login_url="login")
def results(request, sample_id):
    sample = get_object_or_404(Sample, pk=sample_id)
    report_date = sample.report_date
    report_date_error = ""
    user = request.user
    if not user.is_staff:
        organization = user.organization.all()
        if sample.customer not in list(organization):
            raise Http404(f"User not allowed to access analysis reports of {sample.customer}.")
    if request.method == "POST":
        form_is_valid = True
        report_date = request.POST.get('report_date')
        cleaned_report_date = None
        if report_date:
            try:
                cleaned_report_date = parse_datetime(report_date)
            except ValueError:
                form_is_valid = False
            if cleaned_report_date is None:
                form_is_valid = False
        if form_is_valid:
            sample.report_date = cleaned_report_date
            sample.save()
            sample.results.all().delete()
            error = False
            for key, item in request.POST.items():
                if key.startswith("test_") and item != "":
                    test_id = key.split("test_")[-1]
                    test_result = item
                    try:
                        test_method = TestMethod.objects.get(pk=test_id)
                        r = Result.objects.create(sample=sample, test_method=test_method, result=test_result)
                        sample.results.add(r)
                    except TestMethod.DoesNotExist:
                        error = True
            if error:
                msg = "Some results were not updated."
                messages.add_message(request, messages.ERROR, msg)
            else:
                msg = f"<b>{sample}</b> results were updated successfully."
                messages.add_message(request, messages.SUCCESS, msg)
        else:
            report_date_error = "<ul><li>Enter a valid date/time</li></ul>"
    result_list = list()
    for i in sample.product.tests.all():
        result_dict = dict()
        result_dict['id'] = i.id
        result_dict['number'] = i.number
        result_dict['name'] = i.name
        try:
            result_dict['result'] = sample.results.get(test_method=i.id).result
        except Result.DoesNotExist:
            result_dict['result'] = ""
        result_dict['unit'] = i.unit
        if user.is_staff:
            result_list.append(result_dict)
        else:
            if result_dict['result']:
                result_list.append(result_dict)
    if user.is_staff:
        readonly = ""
    else:
        readonly = "readonly"
    if isinstance(report_date, datetime):
        report_date = report_date.strftime("%Y-%m-%dT%H:%M")
    context = {
        'results': result_list,
        'sample': sample,
        'readonly': readonly,
        'report_date': report_date,
        'report_date_error': report_date_error,
    }
    return render(request, "results/details.html", context)
