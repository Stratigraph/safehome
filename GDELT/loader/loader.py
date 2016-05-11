import requests

from import_export import resources
from tablib import Dataset
from . import _md5 as md5

from GDELT.models import GDELTFileResource, GDELTFile
from GDELT.models import Event, EventResource, Actor

import io
import os
from zipfile import ZipFile

from django_cron import CronJobBase, Schedule


'''
1/ Load the list of files into the database
2/ Iterate through list of unimported files
3/ Download zip file
4/ Unzip
5/ Load file
6/ Mark as imported in db
'''

class GDELTLoader() :

	def __init__(self, baseurl, requests=None):
		self.baseurl = baseurl
		self.tmppath = '/tmp'
		if requests is None:
			self.requests = requests.Session()
		else:
			self.requests = requests

	'''
	load of the files found in the md5 file list format
	@url : url of file list
	'''
	def load_file_list(self, url):
		resource = GDELTFileResource()
		filelist = self.requests.get(os.path.join(self.baseurl,url)).text
		dataset = Dataset().load(filelist)
		result = resource.import_data(dataset, dry_run=False)
		return result.has_errors()

	'''
	download all files marked as imported=False
	'''
	def download_files(self):
		files = GDELTFile.objects.filter(imported=False)
		for file in files:
			filename = self.extract_file(file.filename)
			if self.load_file(filename) is True:
				file.imported = True
				file.save()
			os.remove(filename)


	def extract_file(self, url):
		zipfile = ZipFile(io.BytesIO(self.requests.get(os.path.join(self.baseurl,url), timeout=None).content))
		zipfile.extractall(path=self.tmppath)
		return os.path.join(self.tmppath, zipfile.namelist()[0])


	def load_file(self, filename):
		resource = EventResource()
		dataset = Dataset().load(open(filename).read())
		result = resource.import_data(dataset, dry_run=False)
		return result.has_errors()
		

class GDELTLoaderCronJob(CronJobBase):
	RUN_AT_TIMES = ['23:30']
	#RUN_EVERY_MINS = 5
	schedule = Schedule(run_at_times=RUN_AT_TIMES)
	#schedule = Schedule(run_every_mins=RUN_EVERY_MINS) 
	code = 'safehome.GDELT_cron_job'
	
	def do(self):
		loader = GDELTLoader('http://data.gdeltproject.org/events/',requests.Session())
		loader.load_file_list('md5sums')
		loader.download_files()
