from django.contrib.gis import admin

from contacts.models import Contact

class ContactAdmin(admin.OSMGeoAdmin):
	list_display = ('address',)

	
admin.site.register(Contact, ContactAdmin)
