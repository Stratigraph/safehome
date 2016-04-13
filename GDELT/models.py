from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point

from import_export import resources, fields, widgets

class GkgCount(gismodels.Model):
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
			super(GkgCount, self).save(force_insert, force_update)


class GkgCountResource(resources.ModelResource):

	class Meta:
		model = GkgCount
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


class GDELTFile(models.Model):
	md5 = models.CharField(max_length=256)
	filename = models.CharField(max_length=256)
	imported = models.BooleanField(default=False)

	def __unicode__(self):
		return self.filename

class GDELTFileResource(resources.ModelResource):
	
	class Meta:
		model = GDELTFile
		skip_unchanged = True
		report_skipped = False
        
	def before_import(self, dataset, dry_run, **kwargs):
		dataset.headers = ['md5','id','filename',]

class Actor(models.Model):
	Code = models.CharField(max_length=24, null=True)
	Name = models.CharField(max_length=256, null=True)
	CountryCode = models.CharField(max_length=3, null=True)
	KnownGroupCode = models.CharField(max_length=3, null=True)
	EthnicCode = models.CharField(max_length=3, null=True)
	Religion1Code = models.CharField(max_length=3, null=True)
	Religion2Code = models.CharField(max_length=3, null=True)
	Type1Code = models.CharField(max_length=3, null=True)
	Type2Code = models.CharField(max_length=3, null=True)
	Type3Code = models.CharField(max_length=3, null=True)

class Geo(gismodels.Model):
	Type = models.IntegerField()
	FullName = models.CharField(max_length=512, null=True)
	CountryCode = models.CharField(max_length=2, null=True)
	ADM1Code = models.CharField(max_length=4, null=True)
	Lat = models.DecimalField(decimal_places=6, max_digits=9, null=True)
	Long = models.DecimalField(decimal_places=6, max_digits=9, null=True)
	FeatureID = models.CharField(max_length=16, null=True)
	geom = gismodels.PointField(null=True, blank=True)
	

class KnownGroup(models.Model):
	code = models.CharField(max_length=3, unique=True)
	label = models.CharField(max_length=256, unique=True)
	
class KnownGroupResource(resources.ModelResource):
	
	class Meta:
		model = KnownGroup
		skip_unchanged = True
		report_skipped = False
        
	def before_import(self, dataset, dry_run, **kwargs):
		dataset.headers = [str(header).lower().strip() for header in dataset.headers]
		dataset.headers.append('id')
	
	def get_instance(self, instance_loader, row):
		return False
	
class Religion(models.Model):
	code = models.CharField(max_length=3, unique=True)
	label = models.CharField(max_length=256, unique=True)
	
class ReligionResource(resources.ModelResource):
	
	class Meta:
		model = Religion
		skip_unchanged = True
		report_skipped = False
        
	def before_import(self, dataset, dry_run, **kwargs):
		dataset.headers = [str(header).lower().strip() for header in dataset.headers]
		dataset.headers.append('id')
	
	def get_instance(self, instance_loader, row):
		return False
	
class EthnicGroup(models.Model):
	code = models.CharField(max_length=3, unique=True)
	label = models.CharField(max_length=256)
	
class EthnicGroupResource(resources.ModelResource):
	
	class Meta:
		model = EthnicGroup
		skip_unchanged = True
		report_skipped = False
        
	def before_import(self, dataset, dry_run, **kwargs):
		dataset.headers = [str(header).lower().strip() for header in dataset.headers]
		dataset.headers.append('id')
	
	def get_instance(self, instance_loader, row):
		return False
	

class EventCode(models.Model):
	cameoeventcode = models.CharField(max_length=4, unique=True)
	eventdescription = models.CharField(max_length=256, unique=True)
	
class EventCodeResource(resources.ModelResource):
	
	class Meta:
		model = EventCode
		skip_unchanged = True
		report_skipped = False
        
	def before_import(self, dataset, dry_run, **kwargs):
		dataset.headers = [str(header).lower().strip() for header in dataset.headers]
		dataset.headers.append('id')
	
	def get_instance(self, instance_loader, row):
		return False
	
class Country(models.Model):
	code = models.CharField(max_length=3, unique=True)
	label = models.CharField(max_length=256, unique=True)
	
class CountryResource(resources.ModelResource):
	
	class Meta:
		model = Country
		skip_unchanged = True
		report_skipped = False
        
	def before_import(self, dataset, dry_run, **kwargs):
		dataset.headers = [str(header).lower().strip() for header in dataset.headers]
		dataset.headers.append('id')
	
	def get_instance(self, instance_loader, row):
		return False


class Event(gismodels.Model):
	GLOBALEVENTID = models.IntegerField(primary_key=True)
	SQLDATE = models.CharField(max_length=8)

	#MonthYear = models.CharField(max_length=6)
	#Year = models.CharField(max_length=4)
	#FractionDate = models.DecimalField(decimal_places=4, max_digits=8)

	Actor1 = models.ForeignKey('Actor',on_delete=models.CASCADE,related_name='Actor1+',null=True, blank=True)
	Actor1Geo = models.ForeignKey('Geo',on_delete=models.CASCADE,related_name='Actor1Geo+',null=True, blank=True)
	Actor2 = models.ForeignKey('Actor',on_delete=models.CASCADE,related_name='Actor2+',null=True, blank=True)
	Actor2Geo = models.ForeignKey('Geo',on_delete=models.CASCADE,related_name='Actor1Geo+',null=True, blank=True)

	'''
	Actor1Code = models.CharField(max_length=16, null=True)
	Actor1Name = models.CharField(max_length=256, null=True)
	Actor1CountryCode = models.CharField(max_length=3, null=True)
	Actor1KnownGroupCode = models.CharField(max_length=3, null=True)
	Actor1EthnicCode = models.CharField(max_length=3, null=True)
	Actor1Religion1Code = models.CharField(max_length=3, null=True)
	Actor1Religion2Code = models.CharField(max_length=3, null=True)
	Actor1Type1Code = models.CharField(max_length=3, null=True)
	Actor1Type2Code = models.CharField(max_length=3, null=True)
	Actor1Type3Code = models.CharField(max_length=3, null=True)
	Actor2Code = models.CharField(max_length=16, null=True)
	Actor2Name = models.CharField(max_length=256, null=True)
	Actor2CountryCode = models.CharField(max_length=3, null=True)
	Actor2KnownGroupCode = models.CharField(max_length=3, null=True)
	Actor2EthnicCode = models.CharField(max_length=3, null=True)
	Actor2Religion1Code = models.CharField(max_length=3, null=True)
	Actor2Religion2Code = models.CharField(max_length=3, null=True)
	Actor2Type1Code = models.CharField(max_length=3, null=True)
	Actor2Type2Code = models.CharField(max_length=3, null=True)
	Actor2Type3Code = models.CharField(max_length=3, null=True)
	'''
	IsRootEvent = models.BooleanField()

	EventCode = models.ForeignKey('EventCode',on_delete=models.CASCADE,related_name='EventCode',)
	EventBaseCode = models.ForeignKey('EventCode',on_delete=models.CASCADE,related_name='EventBaseCode',)
	EventRootCode = models.ForeignKey('EventCode',on_delete=models.CASCADE,related_name='EventRootCode',)
	QuadClass = models.IntegerField()
	GoldsteinScale = models.DecimalField(decimal_places=1, max_digits=3)
	NumMentions = models.IntegerField()
	NumSources = models.IntegerField()
	NumArticles = models.IntegerField()
	AvgTone = models.DecimalField(decimal_places=12, max_digits=15)
	'''
	Actor1Geo_Type = models.IntegerField()
	Actor1Geo_FullName = models.CharField(max_length=512, null=True)
	Actor1Geo_CountryCode = models.CharField(max_length=2, null=True)
	Actor1Geo_ADM1Code = models.CharField(max_length=4, null=True)
	Actor1Geo_Lat = models.DecimalField(decimal_places=6, max_digits=9, null=True)
	Actor1Geo_Long = models.DecimalField(decimal_places=6, max_digits=9, null=True)
	Actor1Geo_FeatureID = models.CharField(max_length=16, null=True)
	Actor2Geo_Type = models.IntegerField()
	Actor2Geo_FullName = models.CharField(max_length=512, null=True)
	Actor2Geo_CountryCode = models.CharField(max_length=2, null=True)
	Actor2Geo_ADM1Code = models.CharField(max_length=4, null=True)
	Actor2Geo_Lat = models.DecimalField(decimal_places=6, max_digits=9, null=True)
	Actor2Geo_Long = models.DecimalField(decimal_places=6, max_digits=9, null=True)
	Actor2Geo_FeatureID = models.CharField(max_length=16, null=True)
	ActionGeo_Type = models.IntegerField()
	ActionGeo_FullName = models.CharField(max_length=512, null=True)
	ActionGeo_CountryCode = models.CharField(max_length=2, null=True)
	ActionGeo_ADM1Code = models.CharField(max_length=4, null=True)
	ActionGeo_Lat = models.DecimalField(decimal_places=6, max_digits=9, null=True)
	ActionGeo_Long = models.DecimalField(decimal_places=6, max_digits=9, null=True)
	ActionGeo_FeatureID = models.CharField(max_length=16, null=True)
	'''
	ActionGeo = models.ForeignKey('Geo',on_delete=models.CASCADE,related_name='ActionGeo',null=True, blank=True,)
	DATEADDED = models.DateField()
	SOURCEURL = models.URLField(max_length=1024)


class EventResource(resources.ModelResource):

	class Meta:
		model = Event
		'''
		widgets = {
				'SQLDATE': {'format':'%Y%m%d'},
				'DATEADDED': {'format':'%Y%m%d'},
			}
		'''

	def before_import(self, dataset, dry_run, **kwargs):
		dataset.headers = ['GLOBALEVENTID','SQLDATE','MonthYear','Year','FractionDate','Actor1Code','Actor1Name','Actor1CountryCode','Actor1KnownGroupCode','Actor1EthnicCode','Actor1Religion1Code','Actor1Religion2Code','Actor1Type1Code','Actor1Type2Code','Actor1Type3Code','Actor2Code','Actor2Name','Actor2CountryCode','Actor2KnownGroupCode','Actor2EthnicCode','Actor2Religion1Code','Actor2Religion2Code','Actor2Type1Code','Actor2Type2Code','Actor2Type3Code','IsRootEvent','EventCode','EventBaseCode','EventRootCode','QuadClass','GoldsteinScale','NumMentions','NumSources','NumArticles','AvgTone','Actor1Geo_Type','Actor1Geo_FullName','Actor1Geo_CountryCode','Actor1Geo_ADM1Code','Actor1Geo_Lat','Actor1Geo_Long','Actor1Geo_FeatureID','Actor2Geo_Type','Actor2Geo_FullName','Actor2Geo_CountryCode','Actor2Geo_ADM1Code','Actor2Geo_Lat','Actor2Geo_Long','Actor2Geo_FeatureID','ActionGeo_Type','ActionGeo_FullName','ActionGeo_CountryCode','ActionGeo_ADM1Code','ActionGeo_Lat','ActionGeo_Long','ActionGeo_FeatureID','DATEADDED','SOURCEURL',]

	def get_instance(self, instance_loader, row):
		return False

