from django.db import models
from django.db.models.signals import post_save
from django.forms import ModelForm
from datetime import datetime
from django import forms
from django.conf import settings

# Example iPhone JSON:
#
# {
#  "report": {
#    "agency": "Police",
#    "date": "2013-01-04 19:11:03",
#    "description": "papers please!",
#    "latitude": 37.878949500803557,
#    "location": "4th and Market",
#    "longitude": -122.27068675896385,
#    "send_location": 1,
#    "uuid": "9155B656-0EE0-4864-915D-957ECF4B2490"
#  },
#  "user": {
#    "address_1": "123 Fake st",
#    "address_2": "apt 1",
#    "alternate": "123456666939",
#    "city": "Berkeley",
#    "email": "a@a.com",
#    "first_name": "Bob",
#    "last_name": "Smith",
#    "phone": "5555555555",
#    "state": "CA",
#    "zip": "12348"
#  }

class Report(models.Model):

    #########
    ##
    ## Report Information
    ##
    #########

    agency = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField('Date Submitted', blank=True, default=datetime.now)
    location = models.CharField(max_length='200', null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True)

    #########
    ##
    ## Reporter Info
    ##
    #########

    address_1 = models.CharField(max_length=200, blank=True)
    address_2 = models.CharField(max_length=200, blank=True)
    alternate = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=200, blank=True)

    #########
    ##
    ## Internal
    ##
    #########

    approved = models.BooleanField(default=False, blank=True)
    red_flagged = models.BooleanField(default=False, blank=True)
    uuid = models.CharField(max_length=200, blank=True)

class ReportForm(ModelForm):

    class Meta:
        model = Report
        fields = ('agency', 'email', 'location', 'lat', 'lon', 'description',)

    def save(self):
        if not self.instance:
            self.bound_object = Report()
        else:
            self.bound_object = self.instance

        self.bound_object.agency = self.cleaned_data['agency']
        self.bound_object.email = self.cleaned_data['email']
        self.bound_object.location = self.cleaned_data['location']
        self.bound_object.lat = self.cleaned_data['lat']
        self.bound_object.lon = self.cleaned_data['lon']
        self.bound_object.description = self.cleaned_data['description']

        self.bound_object.save()