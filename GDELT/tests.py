from django.test import TestCase

from import_export import resources
from tablib import Dataset
from GDELT.loader.loader import md5, GDELTLoader
import requests
from requests_file import FileAdapter

from GDELT.models import GkgCountResource, GDELTFileResource, GDELTFile
from GDELT.models import Event, EventResource, Actor

class ImportTest(TestCase):
 
	def setUp(self):
		self.requests = requests.Session()
		self.requests.mount('file://', FileAdapter())
		 
	def tearDown(self):
		pass

	def test_import_gdelt_file_list(self):
		resource = GDELTFileResource()
		resource.baseurl = 'file:///code/GDELT/testdata'
		dataset = Dataset().load(self.requests.get('file:///code/GDELT/testdata/md5sums').text)
		result = resource.import_data(dataset, dry_run=False)
		testfile = GDELTFile.objects.get(md5='0f23fc31fb74966f787b7100e8a2a452')
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

	def setUp(self):
		self.requests = requests.Session()
		self.requests.mount('file://', FileAdapter())

	def test_new_file_loader(self):
		loader = GDELTLoader('file:///code/GDELT/testdata/', self.requests)
		loader.load_file_list('md5sums')
		testfile = GDELTFile.objects.get(md5='0f23fc31fb74966f787b7100e8a2a452')
		
	def test_file_loader_extract_file(self):
		loader = GDELTLoader('file:///code/GDELT/testdata/', self.requests)
		loader.load_file_list('md5sums')
		tfile = loader.extract_file('20160405.export.CSV.zip')
		assert(tfile == '/tmp/20160405.export.CSV')

	def test_file_loader_download_files(self):
		loader = GDELTLoader('file:///code/GDELT/testdata/', self.requests)
		loader.load_file_list('md5sums.sml')
		loader.download_files('.export.CSV.zip')
