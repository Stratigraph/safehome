from __future__ import unicode_literals

from django.db import models
from django.contrib.gis.db import models as gismodels
from contacts.models import Contact

class Person(Contact):
	name = models.CharField(max_length=256)
	picture = models.URLField(max_length=256)
	title = models.CharField(max_length=256)

	def __unicode__(self):
		return self.name

	def admin_image(self):
		return '<img src="%s"/>' % self.picture
	admin_image.allow_tags = True
