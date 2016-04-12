from django.contrib.gis import admin

from people.models import Person
from contacts.models import Contact

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin


class PersonResource(resources.ModelResource):
	class Meta:
		model = Person
		fields = ('id', 'name', 'title','picture','address','email','twitter')


class PersonAdmin(ImportExportModelAdmin, admin.OSMGeoAdmin):
	resource_class = PersonResource
	list_display = ('admin_image','name', 'title','address','geom')
	search_fields = ('name',)
	#fields = ('name','title','picture',)

	
admin.site.register(Person, PersonAdmin)
