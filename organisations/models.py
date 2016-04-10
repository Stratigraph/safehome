from __future__ import unicode_literals

from django.db import models
from contacts.models import Contact

# Create your models here.

class Organization(models.Model):
	name = models.CharField(max_length=256)

	def __unicode__(self):
		return self.address

class OrganizationContact(Contact):
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
	
