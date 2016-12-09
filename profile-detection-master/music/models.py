from __future__ import unicode_literals

from django.db import models

class Userdata(models.Model):
	uid = models.IntegerField(primary_key=True)
	name = models.CharField(max_length = 250)
	date = models.DateTimeField()
	pic_url = models.CharField(max_length = 250)

	def __str__(self):
		return self.name

class Record(models.Model):
	uid= models.ForeignKey(Userdata, on_delete= models.CASCADE)
	mrecord= models.IntegerField()
	meeting=models.TextField()
	date1 = models.DateTimeField()

	def __str__(self):
		return self.meeting

