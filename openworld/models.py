from django.db import models
from django.contrib.auth.models import User
from openworld.utils.fields import JSONField

class Source(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False) 
    description = models.CharField(max_length=1024)
    url = models.CharField(max_length=1024)
    phone = models.CharField(max_length=32)
    created_date = models.DateField('date created', auto_now_add=True)
    modified_date = models.DateField('date modified', auto_now=True)

    def __str__(self):
        return self.name

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (i, getattr(self, i))

class Entry(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=512)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=16)
    country = models.CharField(max_length=64)
    tags = JSONField(blank=True, null=True)
    created_date = models.DateField('date created', auto_now_add=True)
    modified_date = models.DateField('date modified', auto_now=True)

    def __str__(self):
        return self.name

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (i, getattr(self, i))

class ExtraEntry(models.Model):
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)
    url = models.CharField(max_length=1024)
    agency = models.CharField(max_length=64)
    agency_url = models.CharField(max_length=1024)
    phone = models.CharField(max_length=32)
    icarol_id = JSONField(blank=True, null=True)

    def __str__(self):
        return self.entry.name

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (i, getattr(self, i))

class Pending(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    source = models.CharField(max_length=64, null=False)
    url = models.CharField(max_length=1024)
    data = JSONField(blank=True, null=False)
    created_date = models.DateField('date created', auto_now_add=True)
    modified_date = models.DateField('date modified', auto_now=True)

    def __str__(self):
        return self.source

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (i, getattr(self, i))

class TagModifications(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    entry = models.ForeignKey(Entry, null=False, on_delete=models.CASCADE)
    tags = JSONField(blank=True, null=False)
    created_date = models.DateField('date created', auto_now_add=True)

    def __str__(self):
        return self.entry.name

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (i, getattr(self, i))
