from django.forms import ModelForm

from reservations.models import Reservation, Restaurant


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ReservationForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"


class RestaurantForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Restaurant
        fields = "__all__"
