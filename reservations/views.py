from django.utils import timezone
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

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса ответа на обратную связь."""
        if request.method == "POST":
            name = request.POST.get("name")  # получаем имя
            message = request.POST.get("message")  # получаем сообщение
            # Отправляем сообщение об успешной отправке
            messages.success(request, f"Спасибо, {name}! Ваше сообщение успешно отправлено.")
            return redirect("reservations:contacts")  # Перенаправляем на ту же страницу
        return render(request, self.template_name)


class Feedback(TemplateView):
    """Шаблон обратной связи."""
    template_name = "reservations/feedback.html"


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
    success_url = reverse_lazy("reservations:reservation_list")
    form_class = ReservationForm

    def get_object(self, queryset=None):
        """Получение одного объекта."""
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        """Добавление данных в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context['form'] = ReservationForm()
        return context

    def get_queryset(self):
        """Набор данных, для отображения в представлении."""

        # Сортируем бронирования по номеру стола
        return Reservation.objects.order_by('table', 'reserved_at')

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса."""
        form = self.form_class(request.POST)

        if form.is_valid():
            reservation = form.save(commit=False)

            # Проверка, находится ли время бронирования в прошлом
            if reservation.reserved_at < timezone.now():
                messages.error(request, "Дата и время бронирования не могут быть в прошлом. Пожалуйста, выберите другое время.")
                return self.get(request, *args, **kwargs)  # Возврат на ту же страницу

            # Если все проверки пройдены, сохраняем бронирование
            reservation.save()
            messages.success(request, "Бронирование создано успешно!")
            return redirect(self.success_url)  # Перенаправление на страницу с успешным бронированием

        # Если форма не прошла валидацию, отправляем общее сообщение об ошибке
        messages.error(request, "Проверьте ваши данные и выберите другое время.")
        return self.get(request, *args, **kwargs)  # Возврат на ту же страницу


class ReservationCreateView(CreateView):
    """Страница создания бронирования."""
    model = Reservation
    form_class = ReservationForm
    template_name = "reservations/reservation_list.html"
    success_url = reverse_lazy("reservations:reservation_list")

    def form_valid(self, form):
        """Обработка данных, если форма прошла валидацию."""

        # Сохраняем объект Reservation
        self.object = form.save()

        # Добавляем сообщение об успешном бронировании
        messages.success(self.request,
                         f"Бронирование столика №{self.object.table.number} на {self.object.reserved_at} успешно создано.")

        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка данных, если форма не прошла валидацию."""

        # Если форма не валидна, показываем ее с ошибками
        return super().form_invalid(form)


class ReservationUpdateView(UpdateView, LoginRequiredMixin):
    """Редактирование бронирования."""

    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("reservations:personal_account")

    def form_valid(self, form):
        """Обработка данных, если форма прошла валидацию."""

        # сохраняем форму
        form.save()
        # Устанавливаем success_url в зависимости от того, редактируем ли мы бронирование
        self.success_url = reverse_lazy("reservations:personal_account")
        return super().form_valid(form)

    def get_object(self, queryset=None):
        """Получение одного объекта."""
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
        """Получение одного объекта."""
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
        """Набор данных, для отображения в представлении."""

        # Фильтруем по владельцу и сортируем по дате и столику
        queryset = Reservation.objects.filter(owner=self.request.user).order_by('reserved_at', 'table')
        return queryset

    def get_object(self, queryset=None):
        """Получение одного объекта."""
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionDenied


class AvailableTablesListView(ListView):
    model = Table
    template_name = 'reservations/reservation_list.html'
    context_object_name = 'available_tables'

    def get_queryset(self):
        """Набор данных, для отображения в представлении."""

        # Получаем текущее время
        now = timezone.now()

        # Находим все столы, которые не забронированы на текущий момент
        reserved_tables = Reservation.objects.filter(
            reserved_at__lte=now,  # Бронирования, которые уже начались
        ).values_list('table_id', flat=True)  # Получаем ID забронированных столов

        # Исключаем забронированные столы из общего списка
        available_tables = Table.objects.exclude(id__in=reserved_tables).filter(is_available=True)
        return available_tables


class Services(TemplateView):
    """Шаблон услуги."""
    template_name = "reservations/services.html"


class Mission(TemplateView):
    """Шаблон миссия и ценности."""
    template_name = "reservations/mission.html"


class Team(TemplateView):
    """Шаблон команда."""
    template_name = "reservations/team.html"