# dental/urls.py

# django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# imports
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

# local
from theblog.admin import blog_adminsite
from events.admin import events_adminsite
#from domeinen.admin import domeinen_adminsite

urlpatterns = [
  # admin urls
  path('admin/', admin.site.urls),
  path('blogadmin/', blog_adminsite.urls),
  path('eventsadmin/', events_adminsite.urls),
  #path('domeinenadmin/', domeinen_adminsite.urls),
  
  # path(users/', include ('django.contrib.auth.urls')),
  
  # App urls
  path('', include('users.urls')),
  path('', include('website.urls')),
  path('', include('stocks.urls')),
  path('', include('theblog.urls')),
  path('', include('events.urls')),
  path('', include('maps.urls', namespace="maps")),
  path('', include('energie.urls')),
  #path('', include('domeinen.urls')),
  path('', include('csvs.urls')),
  path('', include('measurements.urls')),
  #path('', include('verwerkingen.urls')),
  path('', include('meetups.urls')),
  path('', include('photos.urls')),
  path('', include('portfolio.urls')),
  path('', include('store.urls')),
  path('', include('datalab.urls', namespace="datalab")),
  path('', include('rakken.urls', namespace="rakken")),
  # django debug toolbar url
  path('__debug__/', include('debug_toolbar.urls')),
  # OAS urls
  path('schema/', SpectacularAPIView.as_view(), name='schema'),
  path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs')
]

if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # url compositie voor externe toegang tot staticfiles
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # url compositie voor externe toegang tot mediafiles

# Configure Admin area Titles
admin.site.site_header = "Admin area"      # header op admin pagina (blauwe balk)
admin.site.index_title = "Admin van alles" # koptekst op admin pagina en 1e deel in browsertab title
admin.site.site_title  = "Oefenapplicatie" # toevoeging (2e deel) in browsertab title
