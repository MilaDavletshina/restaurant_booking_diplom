from django.urls import path
from . import views
from .views import MainView, Contacts, Message, AboutListView, ReservationListView, ReservationDetailView, \
    ReservationCreateView, ReservationUpdateView, ReservationDeleteView

app_name = 'reservations'

urlpatterns = [
    # path('home/', views.home, name='home'),
    path("", MainView.as_view(), name="main"),
    path("contacts/", Contacts.as_view(), name="contacts"),
    path("message/", Message.as_view(), name="message"),
    path("about/", AboutListView.as_view(), name="about"),

    path("reservation/", ReservationListView(), name="reservation_list"),
    path("reservation/<int:pk>/", ReservationDetailView.as_view(), name="reservation_detail"),
    path("reservation/create/", ReservationCreateView.as_view(), name="reservation_create"),
    path("reservation/<int:pk>/update/", ReservationUpdateView.as_view(), name="reservation_update"),
    path("reservation/<int:pk>/delete/", ReservationDeleteView.as_view(), name="reservation_delete"),
]
