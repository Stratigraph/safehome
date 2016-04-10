import sys, traceback, random
from django.contrib.gis import admin
from django.contrib.gis.geos import Point

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from GDELT.models import GkgCounts

class GkgCountResource(resources.ModelResource):
	#date = fields.Field(column_name='DATE',widget=widgets.DateWidget(format='%Y%m%d'))
	#geo_long = fields.Field(widget=widgets.DecimalWidget())
	#geo_lat = fields.Field(widget=widgets.DecimalWidget())
	#geom = fields.Field()

	class Meta:
		model = GkgCounts
		widgets = {
				'date': {'format':'%Y%m%d'}
			}

	#def dehydrate_geom(self, res):
		#return type(res)
		#return {"type":"Point","coordinates":[res.geo_long,res.geo_lat]}
		#return Point(res.geo_long, res.geo_lat)

	def before_import(self, dataset, dry_run, **kwargs):
		if dataset.headers:
			dataset.headers = [str(header).lower().strip() for header in dataset.headers]
		if 'id' not in dataset.headers:
			dataset.headers.append('id')

	def get_instance(self, instance_loader, row):
		return False

class GDELTAdmin(ImportExportModelAdmin, admin.OSMGeoAdmin):
	resource_class = GkgCountResource
	list_display = ('counttype','number','objecttype','geo_countrycode',)
	search_fields = ('counttype','objecttype','geo_countrycode',)

admin.site.register(GkgCounts, GDELTAdmin)
