import sys, traceback, random
from django.contrib.gis import admin
from django.contrib.gis.geos import Point

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from GDELT.models import GkgCounts, GkgCountResource, GDELTFiles, GDELTFilesResource

class GDELTAdmin(ImportExportModelAdmin, admin.OSMGeoAdmin):
	resource_class = GkgCountResource
	list_display = ('counttype','number','objecttype','geo_countrycode',)
	search_fields = ('counttype','objecttype','geo_countrycode',)

class GDELTFilesAdmin(ImportExportModelAdmin):
	resource_class = GDELTFilesResource

admin.site.register(GkgCounts, GDELTAdmin)
admin.site.register(GDELTFiles, GDELTFilesAdmin)
