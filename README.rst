django-simple-select
====================

.. warning:: This is early early early alpha status. Not tested for... well...
             much of anything. Use at your own risk. API subject to change.

A simple jQueryUI autocomplete <select> replacement for Django.

This project is meant to be a dead simple drop-in replacement for the
Select widget when you have too many objects to sensibly use it.

Features
--------

Good "does nots":

- Doesn't apply styling except on the autocomplete popup list. You get a bare
  text input widget to work with.

- Doesn't require any SQL tables.

- Doesn't require any subclassing to use.

- Doesn't change your POSTdata.

Not-strictly-good "does nots":

- Doesn't look pretty (again, it is focused on having as little styling as
  possible so you can tailor it for your look and feel)

- Doesn't have any MultiSelect functionality (and at this point there are no
  plans for it)

- Doesn't have any API documentation (yet!)

This is in extremely early alpha status; I've only put it on PyPI for the sake
of the project I've created for.

Quickstart
----------
1. ``pip install django-simple-select``

2. Add ``simpleselect`` to ``INSTALLED_APPS`` in your project's
   ``settings.py``.

   .. note:: This is only for the sake of being able to include the JS file. It
            may be possible to remove this step, so it may vanish from a
            future version.

3. Add this to your ``urls.py``

   .. code:: python

        # other urls...
        url('^', include('simpleselect.urls')),
        # ...

4. In your form, make use of a ``simpleselect.AutocompleteSelect`` in a
   ``ModelChoiceField``, e.g.

   .. code:: python

       class MyForm(django.forms.ModelForm):

           class Meta:

               model = models.Person
               widgets = {
                   'employer': simpleselect.AutocompleteSelect(
                       ['name__icontains']),
               }


       class AddPersonForm(django.forms.ModelForm):

           _personwidget = simpleselect.AutocompleteSelect(
               ['first_name__icontains', 'last_name__icontains'])

           person = django.forms.ModelChoiceField(models.Person.objects.all(),
                                                  widget=_personwidget)

   The autocomplete widget takes a list of `Django field lookups`_. When
   autocompleting, it splits the search string. For each individual word, it
   ORs together all lookups applied ot that word. It then ANDs together the
   results of that process applied to all words.

   E.g.: for a widget like

   .. code:: python

    simpleselect.AutocompleteSelect(['first_name__icontains',
                                     'last_name__icontains'])

   and a search string like

   .. code:: python

    "John Smi"

   your final query is equivalent to this, built using `Django Q objects`_:

   .. code:: python

       ((Q(first_name__icontains='John') | Q(last_name__icontains='John'))
        & (Q(first_name__icontains='Smi') | Q(last_name__icontains='Smi')))


   This seems to be the correct thing to do, at least most of the time. But I
   am no expert. More documentation coming!

   .. _Django field lookups: https://docs.djangoproject.com/en/stable/topics/db/queries/#field-lookups
   .. _Django Q objects: https://docs.djangoproject.com/en/stable/topics/db/queries/#complex-lookups-with-q-objects

5. Add this to your template

   .. code:: django

    {% load staticfiles %}

    <script type="text/javascript" src="{% static "simpleselect.js" %}"></script>

6. Unless I forgot something else while writing this, you should be good to go!

Discussion/help
---------------
For now, feel free to message me directly on Github or open a ticket. There's
no mailing list or anything fancy like that. If this picks up any steam I'll
add that stuff.
