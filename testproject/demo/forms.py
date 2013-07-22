from django import forms
import simpleselect

from . import models


class AddEmployeeForm(forms.Form):
    """Really just a farce that lets me play with a different field."""


class CompanyField(simpleselect.AutoSelectField):

    data = models.Company.objects.all()


class PersonForm(forms.ModelForm):

    company = CompanyField()

    class Meta:
        model = models.Person
