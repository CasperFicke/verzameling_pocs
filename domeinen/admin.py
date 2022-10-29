# domeinen/admin.py

# Django
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Local
from .models import (
  Domein,
  Contact,
  Rol,
  Subdomein,
  Certificaattype,
  Certificaat,
  Server,
  Service
  )

# Domeinen admin area
class DomeinenAdminArea(admin.AdminSite):
  site_header = 'Domeinen Admin Area'
  index_title = "Domeinen Admin"
  site_title  = "Oefenapplicatie"

domeinen_adminsite = DomeinenAdminArea(name = 'DomeinenAdmin')

# Models

# Register Server
class ServerAdmin(ImportExportModelAdmin):
  list_display  = ('naam', 'description')
  ordering      = ('naam',)
  list_filter   = ('naam', 'description',)
  search_fields = ('naam', 'description')

# overall admin area 
admin.site.register(Server, ServerAdmin)
# dedicated admin area
domeinen_adminsite.register(Server, ServerAdmin)

# Register Domein
class DomeinAdmin(ImportExportModelAdmin):
  list_display  = ('url', 'website', 'description')
  ordering      = ('url',)
  list_filter   = ('website', 'dnssec')
  search_fields = ('url', 'description')
  fields        = ('url', 'website', ('start', 'end'),
                   'slug', 'description', 'opmerkingen',
                   ('dnsipv4', 'dnsipv6'),
                   ('http', 'https', 'dnssec', 'spf', 'dmarc', 'sts'),
                   'betrokkenen')
  prepopulated_fields = {'slug': ('url',)}
 
# overall admin area 
admin.site.register(Domein, DomeinAdmin)
# dedicated admin area
domeinen_adminsite.register(Domein, DomeinAdmin)

# Register Subdomein
class SubdomeinAdmin(admin.ModelAdmin):
  list_display  = ('url', 'domein', 'description')
  ordering      = ('domein', 'url',)
  list_filter   = ('url', 'domein')
  search_fields = ('url', 'domein')
  fields        = (('url', 'website', 'domein'), ('start', 'end'),
                   'slug', 'description', 'opmerkingen',
                   ('http', 'https', 'dnssec', 'spf', 'dmarc', 'sts'),
                   'betrokkenen')
  prepopulated_fields = {'slug': ('url',)}
 
# overall admin area 
admin.site.register(Subdomein, SubdomeinAdmin)
# dedicated admin area
domeinen_adminsite.register(Subdomein, SubdomeinAdmin)

# Register Contact
class ContactAdmin(admin.ModelAdmin):
  fields        = (('organisatie', 'name'), 'rol', ('adres', 'postcode', 'plaats'), ('telefoon', 'email'))
  list_display  = ('organisatie', 'name', 'rol')
  list_filter   = ('organisatie', 'name', 'rol')
  ordering      = ('rol', 'organisatie')
  search_fields = ('organisatie', 'rol', 'name')

# overall admin area
admin.site.register(Contact, ContactAdmin)
# dedicated admin area
domeinen_adminsite.register(Contact, ContactAdmin)

# Register Models without layout:
myModels = [Rol, Certificaattype, Certificaat, Service]  # iterable list
# overall adminarea
admin.site.register(myModels)
# dedicated admin area
domeinen_adminsite.register(myModels)
