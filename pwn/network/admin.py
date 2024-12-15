from .models import *
from django.contrib import admin

admin.site.site_title = 'MONSTER METERPRETER'
admin.site.site_header = "METERPRETER ADMIN"

admin.site.register(State)
admin.site.register(Target)
admin.site.register(Network)
admin.site.register(Command)
admin.site.register(Log)