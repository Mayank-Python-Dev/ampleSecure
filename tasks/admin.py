from django.contrib import admin
from .models import (
    TaskForRiskCoordinator,
    TaskForFieldExecutive
)

# Register your models here.

admin.site.register(TaskForRiskCoordinator)
admin.site.register(TaskForFieldExecutive)
