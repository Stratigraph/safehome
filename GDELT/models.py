from __future__ import unicode_literals

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
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
	md5 = models.CharField(max_length=256, unique=True)
	filename = models.CharField(max_length=256, unique=True)
	imported = models.BooleanField(default=False)

	def __unicode__(self):
		return self.filename

class GDELTFileResource(resources.ModelResource):
	baseurl = ""
	filename = fields.Field(attribute='filename', column_name='filename')
	
	class Meta:
		model = GDELTFile
		skip_unchanged = True
		report_skipped = False
		import_id_fields = ['md5','filename']
    
	def dehydrate_filename(self, gfile):
		return self.baseurl + gfile.filename

	def before_import(self, dataset, dry_run, **kwargs):
		dataset.headers = ['md5','id','filename',]

class Geo(gismodels.Model):
	Type = models.IntegerField()
	FullName = models.CharField(max_length=512, unique=True)
	CountryCode = models.CharField(max_length=2, null=True)
	ADM1Code = models.CharField(max_length=4, null=True)
	FeatureID = models.CharField(max_length=16, null=True)
	geom = gismodels.PointField(null=True, blank=True)


class Type(models.Model):
	code = models.CharField(max_length=3, unique=True)
	label = models.CharField(max_length=256, unique=True)
	
class TypeResource(resources.ModelResource):
	
	class Meta:
		model = Type
		skip_unchanged = True
		report_skipped = False
        
	def before_import(self, dataset, dry_run, **kwargs):
		dataset.headers = [str(header).lower().strip() for header in dataset.headers]
		dataset.headers.append('id')
	
	def get_instance(self, instance_loader, row):
		return False

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

class Actor(models.Model):
	Uname = models.CharField(max_length=512, unique=True)
	Code = models.CharField(max_length=24)
	Name = models.CharField(max_length=256)
	CountryCode = models.ForeignKey('Country',on_delete=models.CASCADE,null=True, blank=True)
	KnownGroupCode = models.ForeignKey('KnownGroup',on_delete=models.CASCADE,null=True, blank=True)
	EthnicCode = models.ForeignKey('EthnicGroup',on_delete=models.CASCADE,null=True, blank=True)
	Religion1Code = models.ForeignKey('Religion',related_name='Religion1',on_delete=models.CASCADE,null=True, blank=True)
	Religion2Code = models.ForeignKey('Religion',related_name='Religion2',on_delete=models.CASCADE,null=True, blank=True)
	Type1Code = models.ForeignKey('Type',related_name='Type1',on_delete=models.CASCADE,null=True, blank=True)
	Type2Code = models.ForeignKey('Type',related_name='Type2',on_delete=models.CASCADE,null=True, blank=True)
	Type3Code = models.ForeignKey('Type',related_name='Type3',on_delete=models.CASCADE,null=True, blank=True)
	
	@staticmethod
	def from_data(actor, data):
		if data[actor +'Code'] is '':
			return None
		
		uname ='{:s}:{:s}:{:s}:{:s}:{:s}:{:s}:{:s}:{:s}:{:s}:{:s}:{:s}'.format(
			data[actor +'Code'], data[actor +'Name'], data[actor +'CountryCode'], 
			data[actor +'KnownGroupCode'], data[actor +'EthnicCode'], data[actor +'Religion1Code'], 
			data[actor +'Religion2Code'], data[actor +'Type1Code'], data[actor +'Type2Code'], 
			data[actor +'Type3Code'], data[actor +'Geo_ADM1Code'])
			
		try:
			return Actor.objects.get(Uname=uname)
		except ObjectDoesNotExist:
			pass
			
		act = Actor(Uname=uname, Code = data[actor +'Code'], Name = data[actor +'Name'], )
		try: 
			act.CountryCode = Country.objects.get(code=data[actor +'CountryCode'])
		except ObjectDoesNotExist:
			pass
		try: 
			act.KnownGroup = KnownGroup.objects.get(code=data[actor +'KnownGroupCode'])
		except ObjectDoesNotExist:
			pass
		try: 
			act.EthnicCode = EthnicGroup.objects.get(code=data[actor +'EthnicCode'])
		except ObjectDoesNotExist:
			pass
		try: 
			act.Religion1Code = Religion.objects.get(code=data[actor +'Religion1Code'])
			act.Religion2Code = Religion.objects.get(code=data[actor +'Religion2Code'])
		except ObjectDoesNotExist:
			pass
		try: 
			act.Type1Code = Type.objects.get(code=data[actor +'Type1Code'])
			act.Type2Code = Type.objects.get(code=data[actor +'Type2Code'])
			act.Type3Code = Type.objects.get(code=data[actor +'Type3Code'])
		except ObjectDoesNotExist:
			pass

		act.save()
		return act

class Event(gismodels.Model):
	GLOBALEVENTID = models.IntegerField(primary_key=True)
	SQLDATE = models.DateField()

	Actor1 = models.ForeignKey('Actor',on_delete=models.CASCADE,related_name='Actor1+',null=True, blank=True)
	Actor1Geo = models.ForeignKey('Geo',on_delete=models.CASCADE,related_name='Actor1Geo+',null=True, blank=True)
	Actor2 = models.ForeignKey('Actor',on_delete=models.CASCADE,related_name='Actor2+',null=True, blank=True)
	Actor2Geo = models.ForeignKey('Geo',on_delete=models.CASCADE,related_name='Actor1Geo+',null=True, blank=True)

	IsRootEvent = models.BooleanField()

	EventCode = models.ForeignKey('EventCode',on_delete=models.CASCADE,related_name='EventCode',null=True, blank=True)
	EventBaseCode = models.ForeignKey('EventCode',on_delete=models.CASCADE,related_name='EventBaseCode',null=True, blank=True)
	EventRootCode = models.ForeignKey('EventCode',on_delete=models.CASCADE,related_name='EventRootCode',null=True, blank=True)
	QuadClass = models.IntegerField()
	GoldsteinScale = models.DecimalField(decimal_places=1, max_digits=3)
	NumMentions = models.IntegerField()
	NumSources = models.IntegerField()
	NumArticles = models.IntegerField()
	AvgTone = models.DecimalField(decimal_places=12, max_digits=15)
	ActionGeo = models.ForeignKey('Geo',on_delete=models.CASCADE,related_name='ActionGeo',null=True, blank=True,)
	DATEADDED = models.DateField()
	SOURCEURL = models.URLField(max_length=1024)



class EventResource(resources.ModelResource):

	class Meta:
		model = Event
		exclude = ('EventCode','EventBaseCode','EventRootCode', )
		widgets = {
				'SQLDATE': {'format':'%Y%m%d'},
				'DATEADDED': {'format':'%Y%m%d'}
			}


	def before_import(self, dataset, dry_run, **kwargs):
		#if not dry_run:
		dataset.headers = ['GLOBALEVENTID','SQLDATE','MonthYear','Year','FractionDate','Actor1Code','Actor1Name','Actor1CountryCode','Actor1KnownGroupCode','Actor1EthnicCode','Actor1Religion1Code','Actor1Religion2Code','Actor1Type1Code','Actor1Type2Code','Actor1Type3Code','Actor2Code','Actor2Name','Actor2CountryCode','Actor2KnownGroupCode','Actor2EthnicCode','Actor2Religion1Code','Actor2Religion2Code','Actor2Type1Code','Actor2Type2Code','Actor2Type3Code','IsRootEvent','EventCode','EventBaseCode','EventRootCode','QuadClass','GoldsteinScale','NumMentions','NumSources','NumArticles','AvgTone','Actor1Geo_Type','Actor1Geo_FullName','Actor1Geo_CountryCode','Actor1Geo_ADM1Code','Actor1Geo_Lat','Actor1Geo_Long','Actor1Geo_FeatureID','Actor2Geo_Type','Actor2Geo_FullName','Actor2Geo_CountryCode','Actor2Geo_ADM1Code','Actor2Geo_Lat','Actor2Geo_Long','Actor2Geo_FeatureID','ActionGeo_Type','ActionGeo_FullName','ActionGeo_CountryCode','ActionGeo_ADM1Code','ActionGeo_Lat','ActionGeo_Long','ActionGeo_FeatureID','DATEADDED','SOURCEURL',]

	def get_instance(self, instance_loader, row):
		return False

	def get_geo(self, actor, data):
		if data[actor +'Geo_Type'] == '0':
			return None
		try: 
			return Geo.objects.get(FullName=data[actor +'Geo_FullName'])
		except ObjectDoesNotExist:
			if data[actor+'Geo_Lat'] is '' or data[actor+'Geo_Long'] is '':
				return None
			geo = Geo(Type=data[actor +'Geo_Type'], FullName=data[actor +'Geo_FullName'],
					CountryCode=data[actor+'Geo_CountryCode'], ADM1Code=data[actor+'Geo_ADM1Code'],
					FeatureID=data[actor+'Geo_FeatureID'], geom = Point(float(data[actor+'Geo_Long']), float(data[actor+'Geo_Lat'])))
			geo.save()
			return geo

	def save_m2m(self, obj, data, dry_run):
		if dry_run:
			return
		
		obj.Actor1 = Actor.from_data('Actor1', data)
		obj.Actor1Geo = self.get_geo('Actor1', data)
		obj.Actor2 = Actor.from_data('Actor2', data)
		obj.Actor2Geo = self.get_geo('Actor2', data)
		obj.ActionGeo = self.get_geo('Action', data)

		try:
			obj.EventCode = EventCode.objects.get(cameoeventcode=data['EventCode'])
			obj.EventBaseCode = EventCode.objects.get(cameoeventcode=data['EventBaseCode'])
			obj.EventRootCode = EventCode.objects.get(cameoeventcode=data['EventRootCode'])
		except ObjectDoesNotExist:
			pass
