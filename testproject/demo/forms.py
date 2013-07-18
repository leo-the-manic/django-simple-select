from django import forms
import simpleselect.widgets

from . import models


class PersonForm(forms.ModelForm):

    class Meta:
        model = models.Person
        widgets = {
            'company': simpleselect.AutocompleteSelect([])
        }
