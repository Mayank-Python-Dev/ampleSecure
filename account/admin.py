from django.contrib import admin
from .models import (
    User,
    Admin,
    Client,
    SuperAdmin,
    FieldExecutive,
    RiskCoordinator
)

# Register your models here.

class UserModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Client)
admin.site.register(SuperAdmin)
admin.site.register(FieldExecutive)
admin.site.register(RiskCoordinator)

