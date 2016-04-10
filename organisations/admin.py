from django.contrib.gis import admin

from organisations.models import Organization, OrganizationContact
from contacts.models import Contact

class AddressInline(admin.StackedInline):
	model = OrganizationContact


class OrganizationAdmin(admin.OSMGeoAdmin):
	list_display = ('name',)
	search_fields = ('name',)
	fields = ('name',)
	inlines = [
		AddressInline,
	]

	
admin.site.register(Organization, OrganizationAdmin)
