from django.db import models
from django.db.models.signals import post_save
from django.forms import ModelForm
from datetime import datetime
from django import forms
from django.conf import settings

class Report(models.Model):

    # Basics
    title = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
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