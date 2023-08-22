from django.contrib import admin
from .models import (
    User,
    SuperUser,
    Admin,
    RiskCoordinator,
    FieldExecutive,
    Client,
    SuperAdminAndAdmin
)


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username']
    
    @admin.display(description="user type")
    def user_type(self, instance):
        return ", ".join(_.name for _ in instance.groups.all())

    list_display = [
        "uid", "username", "email", "phone_number", "user_type"
    ]


admin.site.register(User, UserAdmin)


class SuperUserAdmin(admin.ModelAdmin):
    search_fields = ['username']

    @admin.display(description="user type")
    def user_type(self, instance):
        return ", ".join(_.name for _ in instance.groups.all())

    list_display = [
        "uid", "username", "email", "phone_number", "user_type"
    ]


admin.site.register(SuperUser, SuperUserAdmin)


class ManagerAdmin(admin.ModelAdmin):
    search_fields = ['username']

    @admin.display(description="user type")
    def user_type(self, instance):
        return ", ".join(_.name for _ in instance.groups.all())

    list_display = [
        "uid", "username", "email", "phone_number", "user_type"
    ]


admin.site.register(Admin, ManagerAdmin)


class RiskCoordinatorAdmin(admin.ModelAdmin):
    search_fields = ['username']

    @admin.display(description="user type")
    def user_type(self, instance):
        return ", ".join(_.name for _ in instance.groups.all())

    list_display = [
        "uid", "username", "email", "phone_number", "user_type"
    ]


admin.site.register(RiskCoordinator, RiskCoordinatorAdmin)


class FieldExecutiveAdmin(admin.ModelAdmin):
    search_fields = ['username']

    @admin.display(description="user type")
    def user_type(self, instance):
        return ", ".join(_.name for _ in instance.groups.all())

    list_display = [
        "uid", "username", "email", "phone_number", "user_type"
    ]


admin.site.register(FieldExecutive, FieldExecutiveAdmin)


class ClientAdmin(admin.ModelAdmin):
    search_fields = ['username']

    @admin.display(description="user type")
    def user_type(self, instance):
        return ", ".join(_.name for _ in instance.groups.all())

    @admin.display(description="client name")
    def client_name(self, instance):
        return instance.username

    list_display = [
        "uid", "client_name", "email", "phone_number", "user_type"
    ]


admin.site.register(Client, ClientAdmin)



class SuperAdminAndManagerAdmin(admin.ModelAdmin):
    # list_filter = ["groups"]
    search_fields = ['username']
    @admin.display(description="user type")
    def user_type(self, instance):
        return ", ".join(_.name for _ in instance.groups.all())

    list_display = [
        "uid", "username", "email", "phone_number", "user_type"
    ]

admin.site.register(SuperAdminAndAdmin, SuperAdminAndManagerAdmin)
