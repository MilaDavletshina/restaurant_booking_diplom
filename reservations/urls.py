from django.urls import path
from reservations.views import (
    MainView,
    Contacts,
    Feedback,
    Message,
    AboutView,
    ReservationListView,
    ReservationUpdateView,
    PersonalAccountListView,
    ReservationCreateView,
    ReservationDeleteView,
)
from reservations.apps import ReservationsConfig


app_name = ReservationsConfig.name

urlpatterns = [
    # path('', home, name='home.html'),
    path("", MainView.as_view(), name="main"),
    path("contacts/", Contacts.as_view(), name="contacts"),
    path("feedback/", Feedback.as_view(), name="feedback"),
    path("message/", Message.as_view(), name="message"),
    path("about/", AboutView.as_view(), name="about"),

    path("reservation/", ReservationListView.as_view(), name="reservation_list"),
    path("reservation/create/", ReservationCreateView.as_view(), name="reservation_create"),
    path("reservation/<int:pk>/update/", ReservationUpdateView.as_view(), name="reservation_update"),
    path("reservation/<int:pk>/delete/", ReservationDeleteView.as_view(), name="reservation_delete"),

    path("personal_account/", PersonalAccountListView.as_view(), name="personal_account"),
]
