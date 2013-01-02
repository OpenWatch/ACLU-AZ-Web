from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, Http404, HttpResponse

def root(request):

    return render_to_response('root.html', { })
