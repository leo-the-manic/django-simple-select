django-simple-select
====================

.. warning:: This is early early early alpha status. API is unstable and it's
             not extensively tested.

A simple jQueryUI autocomplete <select> replacement for Django.

This project is meant to be an easy replacement for the Select widget when
you have too many objects to sensibly use it.

Requirements
------------
- jQuery

- Twitter Bootstrap

- selectize

Features
--------

Good "does nots":

- Doesn't require any SQL tables.

- Doesn't change your POSTdata.

Not-strictly-good "does nots":

- Doesn't have any API documentation (yet!)

This is in extremely early alpha status; I've only put it on PyPI for the sake
of the project I've created for.

Originally there was an intention to have this be a lightweight dependency
(i.e. require not much beyond jQuery), but I've nixed that in favor of me
writing lightweight code. So this at the moment has a hard dependency on both
 Twitter Bootstrap and the selectize library.

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

   .. warning:: This whole step is out of date. From this point on this
                documentation is unreliable. Hopefully I will come back and
                update these docs on my own time.

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

   .. code:: html+django

    {% load staticfiles %}

    <script type="text/javascript" src="{% static "simpleselect.js" %}"></script>

6. Unless I forgot something else while writing this, you should be good to go!

Discussion/help
---------------
For now, feel free to message me directly on Github or open a ticket. There's
no mailing list or anything fancy like that. If this picks up any steam I'll
add that stuff.
