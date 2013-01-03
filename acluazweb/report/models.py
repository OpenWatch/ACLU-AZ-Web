from django.db import models
from django.db.models.signals import post_save
from django.forms import ModelForm
from datetime import datetime
from django import forms
from django.conf import settings

class Report(models.Model):

    # Basics
    title = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField('Date Submitted', blank=True, default=datetime.now)

    # Location
    location = models.CharField(max_length='200')
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    # Moderation
    approved = models.BooleanField(default=False, blank=True)
    red_flagged = models.BooleanField(default=False, blank=True)

    # Text Fields
    description = models.TextField(blank=True)

class ReportForm(ModelForm):

    class Meta:
        model = Report
        fields = ('title', 'email', 'location', 'lat', 'lon', 'description',)

    def save(self):
        if not self.instance:
            self.bound_object = Report()
        else:
            self.bound_object = self.instance

        self.bound_object.title = self.cleaned_data['title']
        self.bound_object.email = self.cleaned_data['email']
        self.bound_object.location = self.cleaned_data['location']
        self.bound_object.lat = self.cleaned_data['lat']
        self.bound_object.lon = self.cleaned_data['lon']
        self.bound_object.description = self.cleaned_data['description']

        self.bound_object.save()