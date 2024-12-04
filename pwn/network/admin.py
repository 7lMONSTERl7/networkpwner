from .models import *
from django.contrib import admin

admin.site.site_title = 'NETWORK POWNER'
admin.site.site_header = "NETWORK ADMIN"

admin.site.register(Network)