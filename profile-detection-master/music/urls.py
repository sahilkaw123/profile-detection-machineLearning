from django.conf.urls import url
from . import views

urlpatterns = [
# /music/
	url(r'^$', views.index, name='index'),

# /music/71/
	url(r'^(?P<uid>[0-9]+)/$', views.detail, name='detail'),	
]
