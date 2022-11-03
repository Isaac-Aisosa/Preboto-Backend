from django.shortcuts import render
from Customer_Care.models import *
from Management.models import Policy, About


# Create your views here.
def index(request):
    location = Location.objects.get(active=True)
    phone = Contact.objects.get(active=True)
    email = Email.objects.get(active=True)
    whatsapp = Whatsapp.objects.get(active=True)
    social = Social.objects.get(active=True)
    app = AppDownloadLink.objects.get(active=True)
    context = {
        'location': location,
        'phone': phone,
        'email': email,
        'whatsapp': whatsapp,
        'social': social,
        'app': app,

    }
    return render(request, 'index.html', context)


def policy(request):
    policie = Policy.objects.filter(active=True).order_by('timestamp')
    context = {
        'policie': policie,
    }
    return render(request, 'policy.html', context)


def about(request):
    abouts = About.objects.filter(active=True).order_by('timestamp')
    context = {
        'abouts': abouts,
    }
    return render(request, 'about.html', context)
