from django.shortcuts import render
# Create your views here.
#from djgeojson.views import GeoJSONLayerView

def index(request):
	return render(request, 'HUD/index.html', {})

