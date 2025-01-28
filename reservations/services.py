from django.utils import timezone
from datetime import timedelta

from reservations.models import Table, Reservation


def check_table_availability(reserved_at, duration_minutes=60):
    """Функция проверки свободного столика"""

    # Получаем время окончания бронирования
    end_time = reserved_at + timedelta(minutes=duration_minutes)

    # Находим все столики
    all_tables = Table.objects.all()

    available_tables = []

    for table in all_tables:
        # Проверяем, есть ли уже бронирование на этот столик в указанный период
        reservations = Reservation.objects.filter(
            table=table,
            reserved_at__lt=end_time,
            reserved_at__gt=reserved_at
        )

        # Если бронирований нет, столик доступен
        if not reservations.exists():
            available_tables.append(table)

    return available_tables


def confirm_reservation(table_id, reserved_at, customer_name, customer_contact):
    """Функция подтверждения бронирования"""

    table = Table.objects.get(id=table_id)

    # Проверяем доступность столика
    available_tables = check_table_availability(reserved_at)

    if table in available_tables:
        # Создаем новое бронирование
        reservation = Reservation(
            table=table,
            reserved_at=reserved_at,
            customer_name=customer_name,
            customer_contact=customer_contact
        )
        reservation.save()
        return reservation
    else:
        raise Exception("Столик недоступен в выбранное время.")