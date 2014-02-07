from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.ForeignKey(Company)

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name,
                                   self.company)
