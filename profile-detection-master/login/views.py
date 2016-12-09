from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
 
# Create your views here.

@login_required
def home(request):
    # execfile('login/test.py')
    #	print a
    return render_to_response(
    'home.html',
    { 'user': '3' }
    )# Create your views here.