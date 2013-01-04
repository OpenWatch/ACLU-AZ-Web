from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, Http404, HttpResponse
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Q

import datetime
time_format = '%Y-%m-%d %H:%M:%S'

import json
import pytz

from report.models import Report, ReportForm

###############
##
## Main list views
##
###############

def root(request):
    reports = Report.objects.filter(red_flagged=False).order_by('-date')

    today = datetime.datetime.today()
    days = datetime.timedelta(days=7)
    begin = today - days
    recent_reports = Report.objects.filter(red_flagged=False).filter(date__range=(begin, today))

    return render_to_response('home.html', { 'reports': reports, 'reportactive': True, 'numtotal': len(reports), 'numweek': len(recent_reports)} , 
        context_instance=RequestContext(request))

def all(request):
    reports = Report.objects.filter().order_by('-date')

    today = datetime.datetime.today()
    days = datetime.timedelta(days=7)
    begin = today - days
    recent_reports = Report.objects.filter(date__range=(begin, today))

    return render_to_response('home.html', { 'reports': reports, 'reportactive': True, 'numtotal': len(reports), 'numweek': len(recent_reports)} , 
        context_instance=RequestContext(request))

def approved(request):
    reports = Report.objects.filter(approved=True).order_by('-date')

    today = datetime.datetime.today()
    days = datetime.timedelta(days=7)
    begin = today - days
    recent_reports = Report.objects.filter(approved=True).filter(date__range=(begin, today))

    return render_to_response('home.html', { 'reports': reports, 'reportactive': True, 'numtotal': len(reports), 'numweek': len(recent_reports)} , 
        context_instance=RequestContext(request))

def search(request, term=None):

    if not term:
        term = str(request.GET['term'])

    if not term:
        return HttpResponseRedirect('/')

    reports = Report.objects.filter(description__icontains=term).order_by('-date')

    today = datetime.datetime.today()
    days = datetime.timedelta(days=7)
    begin = today - days
    recent_reports = Report.objects.filter(description__icontains=term).filter(date__range=(begin, today))

    return render_to_response('home.html', { 'reports': reports, 'reportactive': True, 'numtotal': len(reports), 'numweek': len(recent_reports), 'term': term} , 
        context_instance=RequestContext(request))

##############
##
## Inidividual report views and related
##
#############

def report(request, rid):

    report = get_object_or_404(Report, pk=rid)

    return render_to_response('report.html', { 'report': report, 'reportactive': True, } , 
        context_instance=RequestContext(request))

def approve(request, rid):

    report = get_object_or_404(Report, pk=rid)

    if report.approved:
        report.approved = False
    else:
        report.approved = True
    report.save()

    return HttpResponseRedirect('/r/' + str(report.pk))

def flag(request, rid):

    report = get_object_or_404(Report, pk=rid)

    if report.red_flagged:
        report.red_flagged = False
    else:
        report.red_flagged = True
    report.save()

    return HttpResponseRedirect('/r/' + str(report.pk))

###############
##
## Map
##
###############

def map(request):

    reports = Report.objects.filter(red_flagged=False).filter(~Q(lat=None)).filter(~Q(lon=None)).order_by('-date')

    return render_to_response('map.html', { 'reports': reports, 'mapactive': True }, 
        context_instance=RequestContext(request))

##################
##
## Submission
##
################

def new(request):

    form = ReportForm()

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect('/') 
        else:
            pass
    else:
        form = ReportForm()

    return render_to_response('new.html', { 'form': form }, 
        context_instance=RequestContext(request))

@csrf_exempt
def submit(request):

    if request.method != 'POST':
        return HttpResponse(json.dumps({'success': False, 'reason': 'I only speak POST'}), mimetype='application/json')

    try:
        json_data = json.loads(request.raw_post_data)
    except Exception, e:
        return HttpResponse(json.dumps({'success': False, 'reason': 'Bad JSON.', 'exception': str(e)}), mimetype='application/json')

    try:
        report = Report()
        report.agency = json_data['report'].get('agency', None)
        report.description = json_data['report'].get('description', None)
        report.lat = json_data['report'].get('latitude', None)
        report.lon = json_data['report'].get('longitude', None)
        report.date = string_to_date(json_data['report']['date'])
        report.uuid = json_data['report'].get('uuid', None)
        report.address_1 = json_data['user'].get('address_1', None)
        report.address_2 = json_data['user'].get('address_2', None)
        report.alternate = json_data['user'].get('alternate', None)
        report.first_name = json_data['user'].get('first_name', None)
        report.last_name = json_data['user'].get('last_name', None)
        report.phone = json_data['user'].get('phone', None)
        report.city = json_data['user'].get('city', None)
        report.state = json_data['user'].get('state', None)
        report.zip = json_data['user'].get('zip', None)
        report.save()
    except Exception, e:
        return HttpResponse(json.dumps({'success': False, 'reason': 'Improperly formatted data.', 'exception': str(e) }), mimetype='application/json')

    return HttpResponse(json.dumps({'success': True, 'report_id': report.id }), mimetype='application/json')

##############
##
## Misc
##
#############

def contact(request):

    return render_to_response('contact.html', { 'contactactive': True }, 
        context_instance=RequestContext(request))

#############
##
## Util
##
#############

def string_to_date(time_str):
    date = datetime.datetime.strptime(time_str, time_format)
    tz = pytz.utc
    utc_date = tz.normalize(tz.localize(date))
    return utc_date

def date_to_string(date):
    if date == None:
        return None
    utc_date = date
    if date.tzinfo != None:
        utc_date = date.astimezone(pytz.utc)
    else:
        date.replace(tzinfo=tzutc())
    date_string = utc_date.strftime(time_format)
    return date_string
