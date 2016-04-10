from django.conf.urls import url
from . import views
from djgeojson.views import GeoJSONLayerView
from GDELT.models import GkgCounts

urlpatterns = [
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=GkgCounts), name='data'),
]
