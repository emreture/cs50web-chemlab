from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="login")
def index(request):
    context = {
        'form': form,
    }
    return render(request, "results/index.html", context)


@login_required(login_url="login")
def results(request, sample_id):
    context = {
        'form': form,
    }
    return render(request, "results/details.html", context)
