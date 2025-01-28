from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from reservations.forms import ReservationForm
from reservations.models import Reservation, Restaurant


def home(request):
    """Основной шаблон"""
    return render(request, 'home.html')


class Contacts(TemplateView):
    """Шаблон контакты"""

    template_name = "reservations/contacts.html"

    def contacts(request):
        if request.method == "POST":
            name = request.POST.get("name")  # получаем имя
            message = request.POST.get("message")  # получаем сообщение
            return HttpResponse(f"Спасибо, {name}! {message} Сообщение получено.")
        return render(request, "reservations/contacts.html")


class Feedback(TemplateView):
    """Шаблон обратная связь"""

    template_name = "reservations/feedback.html"


class Message(TemplateView):
    """Страница ответа на отправленное сообщение"""

    template_name = "reservations/message.html"


class MainView(ListView):
    """Главная страница"""
    model = Restaurant
    template_name = "reservations/main.html"


class AboutView(ListView):
    """Страница о ресторане"""

    model = Restaurant
    template_name = "reservations/about.html"


class ReservationListView(ListView):
    """Страница бронирования"""

    model = Reservation


class ReservationDetailView(DetailView, LoginRequiredMixin):
    """Бронирование, просмотр"""

    model = Reservation
    form_class = ReservationForm


class ReservationCreateView(CreateView, LoginRequiredMixin):
    """Бронирование, создание"""

    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("reservations:main")


class ReservationUpdateView(UpdateView, LoginRequiredMixin):
    """Бронирование, обновление"""

    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("reservations:main")


class ReservationDeleteView(DeleteView):
    """Получатель рассылки - удаление"""

    model = Reservation
    success_url = reverse_lazy("reservations:main")