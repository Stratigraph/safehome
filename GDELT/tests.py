from django.test import TestCase

from import_export import resources
from tablib import Dataset
from GDELT.loader import md5, loader
import requests

from GDELT.models import GkgCountResource, GDELTFilesResource

class ImportTest(TestCase):
 
	def setUp(self):
		pass
		 
	def tearDown(self):
		pass
 
	def test_import_gkgcounts(self):
		resource = GkgCountResource()
		dataset = Dataset().load(open('/code/GDELT/testdata/20160405.gkgcounts.sml.csv').read())
		result = resource.import_data(dataset, dry_run=False)
		assert(not result.has_errors())

	def test_import_gdelt_file_list(self):
		resource = GDELTFilesResource()
		dataset = Dataset().load(requests.get('http://data.gdeltproject.org/gkg/md5sums').text)
		result = resource.import_data(dataset, dry_run=False)
		assert(not result.has_errors())

	def test_import_gdelt_file_class(self):
		impt = loader.GDELTLoader()
		impt.load_file_list('http://data.gdeltproject.org/gkg/md5sums')
