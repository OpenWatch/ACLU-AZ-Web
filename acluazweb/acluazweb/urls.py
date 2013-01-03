from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'report.views.root', name='root'),
    url(r'^map/', 'report.views.map', name='map'),
    url(r'^admin/', include(admin.site.urls)),
)
