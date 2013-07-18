from django import forms
import simpleselect

from . import models


class AddEmployeeForm(forms.Form):
    """Really just a farce that lets me play with a different field."""

    person = forms.ModelChoiceField(models.Person.objects.all(),
                                    widget=simpleselect.AutocompleteSelect(
                                        ['first_name__icontains']))


class PersonForm(forms.ModelForm):

    class Meta:
        model = models.Person
        widgets = {
            'company': simpleselect.AutocompleteSelect(['name__icontains'])
        }
