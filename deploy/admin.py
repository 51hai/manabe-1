from django.contrib import admin
from .models import DeployStatus,DeployPool
# Register your models here.

admin.site.register(DeployStatus)
admin.site.register(DeployPool)