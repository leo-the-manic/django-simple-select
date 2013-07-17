# Create your views here.
import django.shortcuts as django

from . import forms


def main(request):
    context = {
        'form': forms.PersonForm()
    }

    return django.render(request, "demo/form.django.html", context)
