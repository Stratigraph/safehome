from django.test import TestCase

from import_export import resources
from tablib import Dataset
from GDELT.loader.loader import md5, GDELTLoader
import requests

from GDELT.models import GkgCountResource, GDELTFileResource, GDELTFile
from GDELT.models import Event, EventResource, Actor

class ImportTest(TestCase):
 
	def setUp(self):
		pass
		 
	def tearDown(self):
		pass

	def test_import_gdelt_file_list(self):
		resource = GDELTFileResource()
		resource.baseurl = 'http://data.gdeltproject.org/gkg/'
		dataset = Dataset().load(requests.get('http://data.gdeltproject.org/gkg/md5sums').text)
		result = resource.import_data(dataset, dry_run=False)
		testfile = GDELTFile.objects.get(md5='039701f6f6ae7f6afc8d414459d52084')
		assert(not result.has_errors())

	def test_import_events(self):
		resource = EventResource()
		dataset = Dataset().load(open('/code/GDELT/testdata/20160405.export.sml.csv').read())
		result = resource.import_data(dataset, dry_run=False)
		
		actor1 = Actor.objects.get(Code='NAMMED')

		assert(actor1.Code == 'NAMMED')
		assert(not result.has_errors())
 
	def test_import_gkgcounts(self):
		resource = GkgCountResource()
		dataset = Dataset().load(open('/code/GDELT/testdata/20160405.gkgcounts.sml.csv').read())
		result = resource.import_data(dataset, dry_run=False)
		assert(not result.has_errors())


class GDELTLoaderTest(TestCase):

	def test_new_file_loader(self):
		loader = GDELTLoader()
		loader.load_file_list('http://data.gdeltproject.org/gkg/md5sums')
		testfile = GDELTFile.objects.get(md5='c8e40ee1b801408cbc52fa382539c46e')
		
	def test_file_loader_load_files(self):
		loader = GDELTLoader()
		loader.load_file_list('http://data.gdeltproject.org/gkg/md5sums')
		loader.download_files('http://data.gdeltproject.org/gkg/')
