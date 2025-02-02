from datetime import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, DeleteView)
from reservations.forms import ReservationForm
from reservations.models import Reservation, Restaurant, Table
from users.models import User


def home(request):
    """Основной шаблон."""
    return render(request, 'home.html')


class Contacts(TemplateView):
    """Шаблон контакты."""
    template_name = "reservations/contacts.html"

    def contacts(request):
        if request.method == "POST":
            name = request.POST.get("name")  # получаем имя
            message = request.POST.get("message")  # получаем сообщение
            return HttpResponse(f"Спасибо, {name}! {message} Сообщение получено.")
        return render(request, "reservations/contacts.html")


class Feedback(TemplateView):
    """Шаблон обратной связи."""
    template_name = "reservations/feedback.html"


class Message(TemplateView):
    """Шаблон ответа на обратную связь."""
    template_name = "reservations/message.html"


class MainView(ListView):
    """Главная страница."""
    model = Restaurant
    template_name = "reservations/main.html"


class AboutView(ListView):
    """Страница о ресторане."""
    model = Restaurant
    template_name = "reservations/about.html"


class ReservationListView(ListView):
    """Страница бронирования."""
    model = Reservation
    template_name = "reservations/reservation_list.html"
    context_object_name = 'reservations'
    form_class = ReservationForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionDenied

    def get_queryset(self):
        # Сортируем бронирования по номеру стола
        return Reservation.objects.order_by('table')


class ReservationCreateView(CreateView):
    """Страница создания бронирования."""
    model = Reservation
    form_class = ReservationForm
    template_name = "reservations/reservation_list.html"
    success_url = reverse_lazy("reservations:reservation_list")

    def form_valid(self, form):
        # Сохраняем объект Reservation
        self.object = form.save()

        # Добавляем сообщение об успешном бронировании
        messages.success(self.request,
                         f"Бронирование столика №{self.object.table.number} на {self.object.reserved_at} успешно создано.")

        return super().form_valid(form)

    def form_invalid(self, form):
        # Если форма не валидна, показываем ее с ошибками
        return super().form_invalid(form)


class ReservationUpdateView(UpdateView, LoginRequiredMixin):
    """Редактирование бронирования."""

    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("reservations:personal_account")

    def form_valid(self, form):
        # сохраняем форму
        form.save()
        # Устанавливаем success_url в зависимости от того, редактируем ли мы бронирование
        self.success_url = reverse_lazy("reservations:personal_account")
        return super().form_valid(form)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionDenied


class ReservationDeleteView(DeleteView):
    """Удаление бронирования."""

    model = Reservation
    success_url = reverse_lazy("reservations:personal_account")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionDenied


class PersonalAccountListView(ListView):
    """Шаблон личного кабинета"""
    model = Reservation
    template_name = "reservations/personal_account.html"

    def get_queryset(self):
        # Фильтруем по владельцу и сортируем по дате и столику
        queryset = Reservation.objects.filter(owner=self.request.user).order_by('reserved_at', 'table')
        return queryset

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionDenied






