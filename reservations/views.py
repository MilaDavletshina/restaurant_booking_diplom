from datetime import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView)
from reservations.forms import ReservationForm
from reservations.models import Reservation, Restaurant

# DetailView, , UpdateView, DeleteView


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


class ReservationCreateView(CreateView):
    """Страница создания бронирования."""
    model = Reservation
    form_class = ReservationForm
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






# class ReservationDetailView(DetailView, LoginRequiredMixin):
#     """Бронирование, просмотр"""
#
#     model = Reservation
#     form_class = ReservationForm
#
#



#
#
# class ReservationUpdateView(UpdateView, LoginRequiredMixin):
#     """Бронирование, обновление"""
#
#     model = Reservation
#     form_class = ReservationForm
#     success_url = reverse_lazy("reservations:main")
#
#
# class ReservationDeleteView(DeleteView):
#     """Получатель рассылки - удаление"""
#
#     model = Reservation
#     success_url = reverse_lazy("reservations:main")


