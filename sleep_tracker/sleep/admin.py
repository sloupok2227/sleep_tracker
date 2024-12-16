from django.contrib import admin
from .models import UserProfile, SleepRecord, PhysicalActivity, DietHabit


# Встроенные записи сна для профиля пользователя
class SleepRecordInline(admin.TabularInline):
    model = SleepRecord
    extra = 0
    fields = ('date', 'sleep_time', 'wake_time', 'wake_ups', 'habits')
    readonly_fields = ('date', 'sleep_time', 'wake_time', 'wake_ups', 'habits')

class PhysicalActivityInline(admin.TabularInline):
    model = PhysicalActivity
    extra = 0
    fields = ('activity_type', 'duration', 'date')  # Удалите 'calories_burned'
    readonly_fields = ('activity_type', 'duration', 'date')  # Удалите 'calories_burned'


class DietHabitInline(admin.TabularInline):
    model = DietHabit
    extra = 0
    fields = ('food', 'calories', 'meal_time', 'date')
    readonly_fields = ('food', 'calories', 'meal_time', 'date')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'date_of_birth')
    inlines = [SleepRecordInline, PhysicalActivityInline, DietHabitInline]


@admin.register(PhysicalActivity)
class PhysicalActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'duration', 'date')  # Удалите 'calories_burned'
    readonly_fields = ('activity_type', 'duration', 'date')  # Удалите 'calories_burned'


@admin.register(DietHabit)
class DietHabitAdmin(admin.ModelAdmin):
    list_display = ('food', 'calories', 'meal_time', 'date', 'profile')
    readonly_fields = ('food', 'calories', 'meal_time', 'date', 'profile')



# Записи сна
@admin.register(SleepRecord)
class SleepRecordAdmin(admin.ModelAdmin):
    def user(self, obj):
        return obj.profile.user.username

    user.short_description = 'Пользователь'
    list_display = ('user', 'date', 'sleep_time', 'wake_time', 'wake_ups', 'habits')
    list_filter = ('profile__user__username', 'date')
    search_fields = ('profile__user__username', 'habits')
