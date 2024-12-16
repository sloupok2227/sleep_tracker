import io
import base64

from django.db.models import Q

from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import SleepRecordForm
from .models import SleepRecord, UserProfile
from datetime import time
from datetime import datetime, timedelta
import csv
from django.http import HttpResponse
import matplotlib.pyplot as plt
from .models import Reminder
from .forms import ReminderForm
from django.shortcuts import render
from .forms import UserRegistrationForm, SleepRecordForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import SleepRecord
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DietHabitForm, PhysicalActivityForm
from .models import DietHabit, PhysicalActivity
from django.http import HttpResponse
from .models import SleepRecord, DietHabit, PhysicalActivity
from django.shortcuts import render, redirect, get_object_or_404
from .models import SleepRecord, Friendship
from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from .models import SleepRecord, Friendship, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import SleepRecord, Friendship
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Friendship, UserProfile
from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Q
from .models import Friendship, SleepRecord
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
import io
import base64
from django.contrib.auth import logout
from django.shortcuts import redirect



@login_required
def add_diet_habit(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = DietHabitForm(request.POST)
        if form.is_valid():
            diet_habit = form.save(commit=False)
            diet_habit.profile = profile
            diet_habit.save()
            return redirect('dashboard')  # Перенаправляем на панель управления
    else:
        form = DietHabitForm()

    return render(request, 'add_diet_habit.html', {'form': form})


@login_required
def add_physical_activity(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = PhysicalActivityForm(request.POST)
        if form.is_valid():
            physical_activity = form.save(commit=False)
            physical_activity.profile = profile
            physical_activity.save()
            return redirect('dashboard')
    else:
        form = PhysicalActivityForm()

    return render(request, 'add_physical_activity.html', {'form': form})


@login_required
def view_diet_habits(request):
    habits = DietHabit.objects.filter(profile=request.user.userprofile)
    return render(request, 'view_diet_habits.html', {'habits': habits})

@login_required
def view_physical_activities(request):
    activities = PhysicalActivity.objects.filter(profile=request.user.userprofile)
    return render(request, 'view_physical_activities.html', {'activities': activities})



# Проверка, является ли пользователь менеджером
def is_manager(user):
    return user.is_staff  # Или любое другое условие для определения менеджера

@user_passes_test(is_manager)
def manager_dashboard(request):
    # Получение данных для отображения
    users = User.objects.all()
    sleep_records = SleepRecord.objects.all()

    return render(request, 'manager_dashboard.html', {
        'users': users,
        'sleep_records': sleep_records,
    })

@login_required
def sort_sleep_records(request):
    # Получаем параметры сортировки
    sort_fields = request.GET.getlist('sort_by')  # Критерии сортировки
    sort_order = request.GET.get('order', 'asc')  # Порядок сортировки (asc или desc)

    # Фильтруем записи текущего пользователя
    records = SleepRecord.objects.filter(profile__user=request.user)

    # Преобразуем записи в список, если требуется сортировка по 'duration'
    if 'duration' in sort_fields:
        records = list(records)  # Преобразуем QuerySet в список для сортировки
        records.sort(
            key=lambda r: r.sleep_duration().total_seconds(),
            reverse=(sort_order == 'desc')
        )

    # Если также выбраны другие критерии (например, wake_ups или date)
    if 'wake_ups' in sort_fields or 'date' in sort_fields:
        query_order = []
        if 'wake_ups' in sort_fields:
            query_order.append('-wake_ups' if sort_order == 'desc' else 'wake_ups')
        if 'date' in sort_fields:
            query_order.append('-date' if sort_order == 'desc' else 'date')

        if isinstance(records, list):
            # Если это список, применяем сортировку вручную
            if 'wake_ups' in sort_fields:
                records.sort(key=lambda r: r.wake_ups, reverse=(sort_order == 'desc'))
            if 'date' in sort_fields:
                records.sort(key=lambda r: r.date, reverse=(sort_order == 'desc'))
        else:
            # Для QuerySet
            records = records.order_by(*query_order)

    return render(request, 'sort_records.html', {
        'records': records,
        'sort_fields': sort_fields,
        'sort_order': sort_order,
    })


def home(request):
    return render(request, 'home.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  # Проверка пользователя
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'login.html')



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Не сохраняем сразу
            user.set_password(form.cleaned_data['password'])  # Шифруем пароль
            user.save()  # Сохраняем пользователя
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def add_sleep_record(request):
    profile = None
    try:
        profile = request.user.userprofile  # Пытаемся получить профиль текущего пользователя
        print(f"DEBUG: Existing profile found -> {profile}")
    except UserProfile.DoesNotExist:
        # Создаём профиль, если его нет
        profile = UserProfile.objects.create(user=request.user)
        print("DEBUG: Created new profile")

    if request.method == 'POST':
        form = SleepRecordForm(request.POST)
        if form.is_valid():
            sleep_record = form.save(commit=False)
            sleep_record.profile = profile  # Привязываем запись к профилю
            sleep_record.save()
            print(f"DEBUG: Saved record for user -> {request.user}")
            return redirect('dashboard')  # Перенаправляем на дашборд
    else:
        form = SleepRecordForm()

    return render(request, 'add_sleep_record.html', {'form': form})


import matplotlib.pyplot as plt
import io
import base64

def generate_sleep_chart(records):
    dates = []
    durations = []

    # Сбор данных для графика
    for record in records:
        if hasattr(record, 'sleep_duration') and callable(record.sleep_duration):
            duration = record.sleep_duration()
            hours = duration.total_seconds() / 3600
            dates.append(record.date)
            durations.append(hours)

    # Проверка данных
    if not dates or not durations:
        print("Ошибка: Невозможно построить график из-за отсутствия данных.")
        return None

    # Настройка стилей графика
    plt.style.use('seaborn-v0_8-whitegrid')  # Современный чистый стиль
    fig, ax = plt.subplots(figsize=(10, 5))

    # Построение графика
    ax.plot(dates, durations, marker='o', color='#4682B4', linewidth=2, markersize=8)  # Цвет линии и маркеров

    # Настройка заголовков и подписей
    ax.set_title('Продолжительность сна', fontsize=14, color='#4682B4', weight='bold')
    ax.set_xlabel('Дата', fontsize=12, color='#555')
    ax.set_ylabel('Часы сна', fontsize=12, color='#555')
    ax.tick_params(axis='both', which='major', labelsize=10, colors='#333')

    # Настройка сетки и фона
    ax.grid(color='#E0E0E0', linestyle='--', linewidth=0.7)
    fig.patch.set_facecolor('#F4F4F9')  # Цвет фона графика
    ax.set_facecolor('#FFFFFF')  # Цвет фона области построения

    # Поворот меток на оси X
    plt.xticks(rotation=45)

    # Обрезка лишнего пространства
    plt.tight_layout()

    # Сохранение графика в base64 для отображения в шаблоне
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    return base64.b64encode(image_png).decode('utf-8')


def custom_logout(request):
    logout(request)
    return redirect('login')  # Перенаправление на страницу входа


@login_required
def dashboard(request):
    profile = request.user.userprofile
    filter_period = request.GET.get('filter', 'all')

    # Инициализация переменных для данных
    sleep_records = SleepRecord.objects.filter(profile=profile)
    diet_habits = DietHabit.objects.filter(profile=profile)
    physical_activities = PhysicalActivity.objects.filter(profile=profile)

    if filter_period == 'week':
        start_date = datetime.today() - timedelta(days=7)
        sleep_records = SleepRecord.objects.filter(profile=profile, date__gte=start_date)
        diet_habits = diet_habits.filter(date__gte=start_date).order_by('-date')
        physical_activities = physical_activities.filter(date__gte=start_date).order_by('-date')
    elif filter_period == 'month':
        start_date = datetime.today() - timedelta(days=30)
        sleep_records = SleepRecord.objects.filter(profile=profile, date__gte=start_date)
        diet_habits = diet_habits.filter(date__gte=start_date).order_by('-date')
        physical_activities = physical_activities.filter(date__gte=start_date).order_by('-date')
    else:
        sleep_records = SleepRecord.objects.filter(profile=profile)
        diet_habits = diet_habits.order_by('-date')
        physical_activities = physical_activities.order_by('-date')

    chart = generate_sleep_chart(sleep_records)
    recommendations = generate_recommendations(sleep_records)

    return render(request, 'dashboard.html', {
        'sleep_records': sleep_records,
        'diet_habits': diet_habits,
        'physical_activities': physical_activities,
        'chart': chart,
        'recommendations': recommendations,
        'filter_period': filter_period,
    })



def generate_recommendations(records):
    if not records:
        return ["Добавьте хотя бы одну запись для получения рекомендаций."]

    # Подсчёт средней продолжительности сна
    total_duration = sum(record.sleep_duration().total_seconds() for record in records)
    avg_duration = total_duration / len(records) / 3600  # Средняя продолжительность сна в часах

    recommendations = []

    # 1. Рекомендации на основе средней продолжительности сна
    if avg_duration < 7:
        recommendations.append("Ваш средний сон меньше 7 часов. Старайтесь спать не менее 7-8 часов в сутки.")
    elif avg_duration > 9:
        recommendations.append("Ваш средний сон больше 9 часов. Попробуйте установить более регулярный график сна.")

    # 2. Рекомендации на основе количества пробуждений
    if any(record.wake_ups > 2 for record in records):
        recommendations.append("Частые пробуждения ночью могут указывать на стресс. Попробуйте расслабляющие упражнения перед сном.")

    # 3. Рекомендации на основе привычек
    for record in records:
        habits = record.habits.lower() if record.habits else ""
        if "телевизор" in habits or "экран" in habits:
            recommendations.append("Избегайте использования телевизора или телефона за час до сна.")
        if "поздно" in habits:
            recommendations.append("Старайтесь ложиться спать раньше, чтобы улучшить качество сна.")

    # Если нет специфических рекомендаций
    if not recommendations:
        recommendations.append("Ваш режим сна выглядит сбалансированным. Продолжайте в том же духе!")

    return recommendations


def test_recommendations(request):
    # Создаём тестовые данные
    today = datetime.today().date()
    test_records = [
        SleepRecord(date=today - timedelta(days=i), sleep_time=time(22, 0), wake_time=time(6, 0), wake_ups=3, habits="Смотрел телевизор")
        for i in range(3)
    ]

    recommendations = generate_recommendations(test_records)
    print("DEBUG: Test Recommendations ->", recommendations)

    return render(request, 'test_recommendations.html', {'recommendations': recommendations})

@login_required
def export_records(request):
    records = SleepRecord.objects.filter(profile__user=request.user).order_by('-date')

    # Создаём CSV-ответ
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sleep_records.csv"'

    writer = csv.writer(response)
    writer.writerow(['Дата', 'Время сна', 'Время пробуждения', 'Количество пробуждений', 'Привычки', 'Длительность сна'])

    for record in records:
        writer.writerow([
            record.date,
            record.sleep_time,
            record.wake_time,
            record.wake_ups,
            record.habits,
            record.sleep_duration()
        ])

    return response
@login_required
def analysis(request):
    records = SleepRecord.objects.filter(profile__user=request.user).order_by('-date')

    # Расчёт средней продолжительности сна
    avg_duration = sum(record.sleep_duration().total_seconds() for record in records) / len(records) / 3600
    best_day = max(records, key=lambda r: r.sleep_duration())
    worst_day = min(records, key=lambda r: r.sleep_duration())

    # Распределение времени сна по дням недели
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    sleep_by_day = {day: 0 for day in days}

    for record in records:
        weekday = record.date.weekday()
        sleep_by_day[days[weekday]] += record.sleep_duration().total_seconds() / 3600

    # Генерация диаграммы
    plt.figure(figsize=(8, 5))
    plt.bar(sleep_by_day.keys(), sleep_by_day.values(), color='blue')
    plt.title('Распределение времени сна по дням недели')
    plt.xlabel('День недели')
    plt.ylabel('Среднее время сна (часы)')
    plt.tight_layout()

    # Сохранение диаграммы
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    chart = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'analysis.html', {
        'avg_duration': avg_duration,
        'chart': chart,
        'best_day': best_day,
        'worst_day': worst_day,
    })

@login_required
def manage_reminders(request):
    reminders = Reminder.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            return redirect('manage_reminders')
    else:
        form = ReminderForm()

    return render(request, 'manage_reminders.html', {'form': form, 'reminders': reminders})




# Отправка запроса в друзья
@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    Friendship.objects.get_or_create(from_user=request.user, to_user=to_user)
    return redirect('friends_list')


# Просмотр входящих запросов в друзья
@login_required
def friend_requests(request):
    incoming_requests = Friendship.objects.filter(to_user=request.user, accepted=False)
    return render(request, 'friend_requests.html', {'friend_requests': incoming_requests})

# Принятие или отклонение запросов
@login_required
def handle_friend_request(request, friendship_id, action):
    friendship = get_object_or_404(Friendship, id=friendship_id, to_user=request.user)
    if action == 'accept':
        friendship.accepted = True
        friendship.save()
    elif action == 'decline':
        friendship.delete()
    return redirect('friend_requests')


# Принятие запроса в друзья
@login_required
def accept_friend_request(request, user_id):
    friend_request = get_object_or_404(Friendship, from_user_id=user_id, to_user=request.user)
    friend_request.accepted = True
    friend_request.save()
    return redirect('friends_list')

# Список друзей


@login_required
def friends_list(request):
    user = request.user
    # Получаем список друзей и запросов в друзья
    friendships = Friendship.objects.filter(
        Q(from_user=user) | Q(to_user=user)
    ).select_related('from_user', 'to_user')

    return render(request, 'friends_list.html', {'friends': friendships})



# Общедоступные записи
@login_required
def public_sleep_records(request):
    sort_fields = request.GET.getlist('sort_by')
    sort_order = request.GET.get('order', 'asc')

    # Получение всех общественных записей
    records = list(SleepRecord.objects.filter(visibility='public').select_related('profile__user'))

    # Сортировка
    if 'duration' in sort_fields:
        records = sorted(
            records,
            key=lambda x: x.sleep_duration(as_dict=True)['hours'] * 60 + x.sleep_duration(as_dict=True)['minutes'],
            reverse=(sort_order == 'desc')
        )
        sort_fields.remove('duration')

    if sort_fields:
        records = sorted(
            records,
            key=lambda x: tuple(getattr(x, field) for field in sort_fields),
            reverse=(sort_order == 'desc')
        )

    return render(request, 'public_sleep_records.html', {
        'records': records,
        'sort_fields': sort_fields,
        'sort_order': sort_order,
    })




# Данные друзей
@login_required
def friends_sleep_records(request):
    sort_fields = request.GET.getlist('sort_by')
    sort_order = request.GET.get('order', 'asc')

    # Получение друзей пользователя
    friendships = Friendship.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user),
        accepted=True
    )
    friend_users = [
        friendship.to_user if friendship.from_user == request.user else friendship.from_user
        for friendship in friendships
    ]

    friend_profiles = UserProfile.objects.filter(user__in=friend_users)

    # Получение записей друзей
    records = list(SleepRecord.objects.filter(profile__in=friend_profiles, visibility='friends'))

    # Сортировка
    if 'duration' in sort_fields:
        records = sorted(
            records,
            key=lambda x: x.sleep_duration(as_dict=True)['hours'] * 60 + x.sleep_duration(as_dict=True)['minutes'],
            reverse=(sort_order == 'desc')
        )
        sort_fields.remove('duration')

    if sort_fields:
        records = sorted(
            records,
            key=lambda x: tuple(getattr(x, field) for field in sort_fields),
            reverse=(sort_order == 'desc')
        )

    return render(request, 'friends_sleep_records.html', {
        'records': records,
        'sort_fields': sort_fields,
        'sort_order': sort_order,
    })


@login_required
def user_list(request):
    # Исключаем текущего пользователя
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'user_list.html', {'users': users})

@login_required
def users_list(request):
    # Получаем всех пользователей, кроме текущего
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'users_list.html', {'users': users})
