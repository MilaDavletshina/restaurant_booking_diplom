from django.contrib import admin
from .models import Reservation, Restaurant, Contact


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "restaurant", "date", "guests", "status")
    list_filter = ("user", "restaurant", )
    search_fields = ("user", "restaurant", )


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "message")
    list_filter = ("name",)
    search_fields = ("user", "email",)
