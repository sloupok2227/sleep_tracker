
from django.contrib.auth.models import User
from django import forms
from .models import SleepRecord
from django import forms
from django.contrib.auth.models import User
from django import forms
from .models import Reminder
from django import forms
from .models import SleepRecord
from django import forms
from .models import DietHabit, PhysicalActivity
from django import forms
from .models import DietHabit, PhysicalActivity
from django import forms
from .models import SleepRecord


class DietHabitForm(forms.ModelForm):
    class Meta:
        model = DietHabit
        fields = ['food', 'calories', 'meal_time', 'date']
        widgets = {
            'food': forms.Select(choices=[
                ('Яблоко', 'Яблоко'),
                ('Банан', 'Банан'),
                ('Хлеб', 'Хлеб'),
                ('Молоко', 'Молоко'),
            ]),
            'calories': forms.NumberInput(attrs={'placeholder': 'Введите количество калорий'}),
            'meal_time': forms.TimeInput(attrs={'type': 'time'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class PhysicalActivityForm(forms.ModelForm):
    class Meta:
        model = PhysicalActivity
        fields = ['activity_type', 'duration', 'date']
        widgets = {
            'activity_type': forms.Select(choices=[
                ('Бег', 'Бег'),
                ('Плавание', 'Плавание'),
                ('Йога', 'Йога'),
                ('Тренажерный зал', 'Тренажерный зал')
            ]),
            'duration': forms.TimeInput(attrs={'type': 'time'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают.')
        return cleaned_data



from django import forms
from .models import SleepRecord
from django.forms.widgets import DateInput, TimeInput

class SleepRecordForm(forms.ModelForm):
    class Meta:
        model = SleepRecord
        fields = ['date', 'sleep_time', 'wake_time', 'wake_ups', 'habits', 'visibility']  # Добавляем поле visibility
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'sleep_time': forms.TimeInput(attrs={'type': 'time'}),
            'wake_time': forms.TimeInput(attrs={'type': 'time'}),
            'habits': forms.Textarea(attrs={'placeholder': 'Введите ваши привычки, связанные со сном'}),
            'visibility': forms.Select(choices=SleepRecord.visibility_choices),  # Добавляем выпадающий список
        }

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['reminder_time', 'message']