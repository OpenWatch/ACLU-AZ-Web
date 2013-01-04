from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, Http404, HttpResponse
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Q

import datetime
import json

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
        return HttpResponse("{'success': false, 'reason': 'I only speak POST'}", mimetype='application/json')

    try:
        json_data = json.loads(request.raw_post_data)
    except Exception, e:
        return HttpResponse("{'success': false, 'reason': 'Bad JSON.', 'exception': '" + str(e) + "'}", mimetype='application/json')

    try:
        report = Report()
        report.agency = json_data['report']['agency']
        report.description = json_data['report']['description']
        report.lat = json_data['report']['latitude']
        report.lon = json_data['report']['longitude']
        report.uuid = json_data['report']['uuid']
        report.address_1 = json_data['user']['address_1']
        report.address_2 = json_data['user']['address_2']
        report.alternate = json_data['user']['alternate']
        report.first_name = json_data['user']['first_name']
        report.last_name = json_data['user']['last_name']
        report.phone = json_data['user']['phone']
        report.city = json_data['user']['city']
        report.state = json_data['user']['state']
        report.zip = json_data['user']['zip']
        report.save()
    except Exception, e:
        return HttpResponse("{'success': false, 'reason': 'Improperly formatted data.', 'exception': '" + str(e) + "'}", mimetype='application/json')

    return HttpResponse("{'success': true, 'report_id': " + str(report.id) + "}", mimetype='application/json')

##############
##
## Misc
##
#############

def contact(request):

    return render_to_response('contact.html', { 'contactactive': True }, 
        context_instance=RequestContext(request))
