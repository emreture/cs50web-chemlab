from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, Http404
from samples.models import Sample
from django.conf import settings

# Create your views here.


@login_required(login_url="login")
def index(request):
    query = request.GET.get('q')
    page_number = request.GET.get('page')
    user = request.user
    organization = user.organization.all()
    print(organization)
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
        'query': query,
    }
    return render(request, "results/index.html", context)


@login_required(login_url="login")
def results(request, sample_id):
    user = request.user
    sample = get_object_or_404(Sample, pk=sample_id)
    if not user.is_staff:
        organization = user.organization.all()
        if sample.customer not in list(organization):
            raise Http404(f"User not allowed to access analysis reports of {sample.customer}.")
    print(sample.results.all())
    form = None
    context = {
        'form': form,
    }
    return render(request, "results/details.html", context)
