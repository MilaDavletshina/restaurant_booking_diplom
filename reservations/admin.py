from django.contrib import admin
from .models import Reservation, Restaurant, Contact, Table


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "reserved_at", "customer_name", "customer_contact")
    list_filter = ("customer_name", "reserved_at", )
    search_fields = ("customer_name", "reserved_at", )


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "history", "mission")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "message")
    list_filter = ("name",)
    search_fields = ("user", "email",)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "capacity")
    list_filter = ("number",)
    search_fields = ("number",)
