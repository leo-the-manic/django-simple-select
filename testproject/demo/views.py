# Create your views here.
import django.shortcuts as django

from . import forms


def main(request):
    """Show two unsubmittable test forms."""
    context = {
        'form': forms.PersonForm(),
        'form2': forms.AddEmployeeForm(),
    }

    return django.render(request, "demo/form.django.html", context)
