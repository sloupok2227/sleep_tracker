from datetime import timedelta, datetime
from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class DietHabit(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="diet_habits")
    food = models.CharField(max_length=255)
    meal_time = models.TimeField()
    calories = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.food} - {self.profile.user.username}"


class PhysicalActivity(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="physical_activities")
    activity_type = models.CharField(max_length=255)
    duration = models.DurationField()
    date = models.DateField()

    def __str__(self):
        return f"{self.activity_type} - {self.profile.user.username}"


class SleepRecord(models.Model):
    visibility_choices = [
        ('private', 'Только я'),
        ('friends', 'Друзья'),
        ('public', 'Все'),
    ]

    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField()
    sleep_time = models.TimeField()
    wake_time = models.TimeField()
    wake_ups = models.IntegerField()
    habits = models.TextField(null=True, blank=True)
    visibility = models.CharField(
        max_length=10,
        choices=visibility_choices,
        default='private'
    )

    def sleep_duration(self, as_dict=False):
        from datetime import datetime, timedelta
        sleep_datetime = datetime.combine(self.date, self.sleep_time)
        wake_datetime = datetime.combine(self.date, self.wake_time)
        if wake_datetime <= sleep_datetime:
            wake_datetime += timedelta(days=1)
        total_duration = wake_datetime - sleep_datetime

        if as_dict:
            hours = total_duration.seconds // 3600
            minutes = (total_duration.seconds // 60) % 60
            return {'hours': hours, 'minutes': minutes}
        return total_duration

    def __str__(self):
        return f"SleepRecord for {self.profile.user.username} on {self.date}"





class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friendship_requests_received', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({'Accepted' if self.accepted else 'Pending'})"

    class Meta:
        unique_together = ('from_user', 'to_user')

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reminder_time = models.TimeField()
    message = models.CharField(max_length=255, default="Пора ложиться спать!")
