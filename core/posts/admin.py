from django.contrib import admin
from . import models
from django.apps import apps

# Register your models here.

admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Like)

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)
