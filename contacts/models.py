from __future__ import unicode_literals

from django.db import models
from django.contrib.gis.db import models as gismodels

import csv, urllib, json
from django.contrib.gis.geos import Point
from django.utils.encoding import smart_str

class Contact(gismodels.Model):
	address = models.CharField(max_length=256, null=True, blank=True)
	phone_1 = models.CharField(max_length=16, null=True, blank=True)
	phone_2 = models.CharField(max_length=16, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	web = models.URLField(null=True, blank=True)
	twitter = models.CharField(max_length=256, null=True, blank=True)
	facebook = models.CharField(max_length=256, null=True, blank=True)
	skype = models.CharField(max_length=256, null=True, blank=True)
	
	geom = gismodels.PointField(null=True, blank=True)
	#objects = gismodels.GeoManager()

	def __unicode__(self):
		return self.address

	def geocode(self):
		result = {}
		location = urllib.parse.quote_plus(smart_str(self.address))
		url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % location
		response = urllib.request.urlopen(url).read() 
		result = json.loads(response.decode('utf-8'))
		if result['status'] == 'OK':
			self.geom=Point(
				float(result['results'][0]['geometry']['location']['lng']),
				float(result['results'][0]['geometry']['location']['lat']))

	def save(self, force_insert=False, force_update=False):
		if self.address is not None:
			self.geocode()
		super(Contact, self).save(force_insert, force_update)

