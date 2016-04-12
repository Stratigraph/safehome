import requests

from import_export import resources
from tablib import Dataset
from . import _md5 as md5

from GDELT.models import GDELTFilesResource, GDELTFiles

class GDELTLoader(object) :

	def load_file_list(self, url):
		filelist = requests.get(url).text
		resource = GDELTFilesResource()
		dataset = Dataset().load(filelist)
		result = resource.import_data(dataset, dry_run=False)

	def download_files(self, baseurl):
		files = GDELTFiles.objects.filter(imported=False)
		for file in files:
			zip = requests.get(url+'/'+file.filename)
			
