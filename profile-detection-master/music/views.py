#from django.http import Http404
#from django.shortcuts import render
#from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from models import Userdata
import requests
from app import getImg


def index(request):
	all_userdata = Userdata.objects.all()
	
	#context = {'all_userdata': all_userdata}
	return render(request, 'music/index.html', {'all_userdata': all_userdata})


def detail(request, uid):
	#try:
	#	uid = Userdata.objects.get(uid=uid)
	#except Userdata.DoesNotExist:
	#	raise Http404("Student does not exist")
	id_v = 21
	id_v = request.GET['cID']
	s = getImg.getInfo(id_v)
	uid = get_object_or_404(Userdata, uid=uid)
	return render(request, 'music/detail.html', {'uid': uid, 'id':s.id, 'imgUrl':s.imgUrl, 'name':s.name })
	#return HttpResponse("<h2>Details for Student: " + str(uid)+ "</h2>")
	