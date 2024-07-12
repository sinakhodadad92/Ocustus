from django.contrib import admin
from .models import Job, Panel, Error
# Register your models here.
admin.site.register(Job)
admin.site.register(Panel)
#admin.site.register(Board)
admin.site.register(Error)
