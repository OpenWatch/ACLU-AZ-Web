from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, Http404, HttpResponse
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render_to_response

from report.models import Report, ReportForm

def root(request):

    reports = Report.objects.filter(red_flagged=False)

    return render_to_response('home.html', { 'reports': reports, 'reportactive': True, 'numtotal': len(reports), 'numweek': 0} , 
        context_instance=RequestContext(request))

def all(request):

    reports = Report.objects.filter()

    return render_to_response('home.html', { 'reports': reports, 'reportactive': True, 'numtotal': len(reports), 'numweek': 0} , 
        context_instance=RequestContext(request))

def approved(request):

    reports = Report.objects.filter(approved=True)

    return render_to_response('home.html', { 'reports': reports, 'reportactive': True, 'numtotal': len(reports), 'numweek': 0} , 
        context_instance=RequestContext(request))

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

def map(request):

    return render_to_response('map.html', { 'mapactive': True }, 
        context_instance=RequestContext(request))

def contact(request):

    return render_to_response('contact.html', { 'contactactive': True }, 
        context_instance=RequestContext(request))

def new(request):

    form = ReportForm()

    if request.method == 'POST': # If the form has been submitted...
        form = ReportForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect('/') # Redirect after POST
        else:
            pass
            #print "Shiiiiit"
    else:
        form = ReportForm()

    return render_to_response('new.html', { 'form': form }, 
        context_instance=RequestContext(request))
