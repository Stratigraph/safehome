import sys, traceback, random
from django.contrib.gis import admin
from django.contrib.gis.geos import Point

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from GDELT.models import GkgCount, GkgCountResource, GDELTFile, GDELTFileResource
from GDELT.models import Geo, Event, EventResource, Actor, KnownGroup, KnownGroupResource
from GDELT.models import Religion, ReligionResource, EventCode, EventCodeResource
from GDELT.models import EthnicGroup, EthnicGroupResource, Country, CountryResource

class GDELTAdmin(ImportExportModelAdmin, admin.OSMGeoAdmin):
	resource_class = GkgCountResource
	list_display = ('counttype','number','objecttype','geo_countrycode',)
	search_fields = ('counttype','objecttype','geo_countrycode',)

class GDELTFilesAdmin(ImportExportModelAdmin):
	resource_class = GDELTFileResource

class EventAdmin(ImportExportModelAdmin, admin.OSMGeoAdmin):
	resource_class = EventResource

class KnownGroupAdmin(ImportExportModelAdmin, admin.OSMGeoAdmin):
	resource_class = KnownGroupResource
	list_display = ('code','label',)
	search_fields = ('code','label',)

class ReligionAdmin(ImportExportModelAdmin, admin.OSMGeoAdmin):
	resource_class = ReligionResource
	list_display = ('code','label',)
	search_fields = ('code','label',)

class EthnicGroupAdmin(ImportExportModelAdmin, admin.OSMGeoAdmin):
	resource_class = EthnicGroupResource
	list_display = ('code','label',)
	search_fields = ('code','label',)

class EventCodeAdmin(ImportExportModelAdmin, admin.OSMGeoAdmin):
	resource_class = EventCodeResource
	list_display = ('cameoeventcode','eventdescription',)
	search_fields = ('cameoeventcode','eventdescription',)

class CountryAdmin(ImportExportModelAdmin, admin.OSMGeoAdmin):
	resource_class = CountryResource
	list_display = ('code','label',)
	search_fields = ('code','label',)

admin.site.register(GkgCount, GDELTAdmin)
admin.site.register(GDELTFile, GDELTFilesAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(KnownGroup, KnownGroupAdmin)
admin.site.register(Religion, ReligionAdmin)
admin.site.register(EventCode, EventCodeAdmin)
admin.site.register(EthnicGroup, EthnicGroupAdmin)
admin.site.register(Country, CountryAdmin)
