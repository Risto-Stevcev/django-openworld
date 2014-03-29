from django.contrib import admin
from openworld.models import Source, Entry, ExtraEntry, Pending

admin.site.register(Source)
admin.site.register(Entry)
admin.site.register(ExtraEntry)
admin.site.register(Pending)
