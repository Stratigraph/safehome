from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point

from import_export import resources, fields, widgets

class GkgCounts(gismodels.Model):
	date = models.DateField()
	numarts = models.IntegerField()
	counttype = models.CharField(max_length=128)
	number = models.CharField(max_length=128)
	objecttype = models.CharField(max_length=128)
	geo_type = models.IntegerField()
	geo_fullname = models.CharField(max_length=256)
	geo_countrycode = models.CharField(max_length=2)
	geo_adm1code = models.CharField(max_length=4)
	geo_lat = models.DecimalField(decimal_places=6, max_digits=9, null=True)
	geo_long = models.DecimalField(decimal_places=6, max_digits=9, null=True)
	geo_featureid = models.CharField(max_length=256)
	#cameoeventids = models.CommaSeparatedIntegerField(max_length=4096)
	sources = models.TextField()
	sourceurls = models.TextField()
	geom = gismodels.PointField(null=True, blank=True)

	def __unicode__(self):
		return self.counttype

	def save(self, force_insert=False, force_update=False):
		if self.geo_lat is not None:
			self.geom=Point(float(self.geo_long), float(self.geo_lat))
			super(GkgCounts, self).save(force_insert, force_update)


class GkgCountResource(resources.ModelResource):

	class Meta:
		model = GkgCounts
		widgets = {
				'date': {'format':'%Y%m%d'}
			}

	def before_import(self, dataset, dry_run, **kwargs):
		if dataset.headers:
			dataset.headers = [str(header).lower().strip() for header in dataset.headers]
		if 'id' not in dataset.headers:
			dataset.headers.append('id')

	def get_instance(self, instance_loader, row):
		return False


class GDELTFiles(models.Model):
	md5 = models.CharField(max_length=256)
	filename = models.CharField(max_length=256)
	imported = models.BooleanField(default=False)

	def __unicode__(self):
		return self.filename

class GDELTFilesResource(resources.ModelResource):
	
	class Meta:
		model = GDELTFiles
		skip_unchanged = True
		report_skipped = False
        
	def before_import(self, dataset, dry_run, **kwargs):
		dataset.headers = ['md5','id','filename',]

