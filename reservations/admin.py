from django.contrib import admin
from .models import Reservation, Contact


@admin.register(Reservation)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "table_number")
    list_filter = ("user", "table_number",)
    search_fields = ("user", "table_number",)


@admin.register(Contact)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("user", "email",)
