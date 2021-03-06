from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'report.views.root', name='root'),
    url(r'^map/', 'report.views.map', name='map'),
    url(r'^new/', 'report.views.new', name='new'),
    url(r'^submit/', 'report.views.submit', name='submit'),
    url(r'^all/', 'report.views.all', name='all'),
    url(r'^search/', 'report.views.search', name='search'),
    url(r'^search/(?P<term>[a-zA-Z0-9_. -]+)', 'report.views.search', name='search'),
    url(r'^approved/', 'report.views.approved', name='approved'),
    url(r'^contact/', 'report.views.contact', name='contact'),
    url(r'^r/(?P<rid>[a-zA-Z0-9_. -]+)', 'report.views.report', name='report'),
    url(r'^approve/(?P<rid>[a-zA-Z0-9_. -]+)', 'report.views.approve', name='approve'),
    url(r'^flag/(?P<rid>[a-zA-Z0-9_. -]+)', 'report.views.flag', name='flag'),

    url(r'^admin/', include(admin.site.urls)),


)
