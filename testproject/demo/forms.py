from django import forms
import simpleselect

from . import models


class PersonField(simpleselect.AutoSelectField):

    queries = ['first_name__icontains', 'last_name__icontains']

    data = models.Person.objects.all()


class AddEmployeeForm(forms.Form):
    """Really just a farce that lets me play with a different field."""

    person = PersonField(initial=10, help_text="Should have an initial value.")


class CompanyField(simpleselect.AutoSelectField):

    queries = ['name__icontains']

    data = models.Company.objects.all()


class PersonForm(forms.ModelForm):

    company = CompanyField()

    class Meta:
        model = models.Person
