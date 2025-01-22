from django.contrib import admin
from .models import Reservation, Contact


@admin.register(Reservation)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "guests", "status")
    list_filter = ("user",)
    search_fields = ("user",)


@admin.register(Contact)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "message")
    list_filter = ("name",)
    search_fields = ("user", "email",)
