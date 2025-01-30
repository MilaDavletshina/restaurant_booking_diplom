from django.forms import ModelForm, DateTimeField, DateInput
from reservations.models import Reservation, Restaurant
from django import forms


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class RestaurantForm(StyleFormMixin, ModelForm):
    """Форма создания нового ресторана."""
    class Meta:
        model = Restaurant
        fields = "__all__"


class ReservationForm(ModelForm):
    """Форма бронирования столика."""

    class Meta:
        """Стилизация формы бронирования столика."""
        model = Reservation
        fields = ["table", 'reserved_at', 'customer_name', "customer_contact"]
        widgets = {
            'reserved_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите дату и время',
                'type': 'datetime-local'  # для выбора даты и времени
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields["table"].widget.attrs.update({'class': 'form-control'})
        self.fields["customer_name"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Уточните Ваше имя'})
        self.fields["customer_contact"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите контактную информацию'})

