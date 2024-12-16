from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import custom_logout

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('register/', views.register, name='register'),
    path('add/', views.add_sleep_record, name='add_sleep_record'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Вход
    path('logout/', custom_logout, name='logout'),
    path('test-recommendations/', views.test_recommendations, name='test_recommendations'),
    path('export/', views.export_records, name='export_records'),
    path('analysis/', views.analysis, name='analysis'),
    path('reminders/', views.manage_reminders, name='manage_reminders'),
    path('sort/', views.sort_sleep_records, name='sort_records'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('view-diet-habits/', views.view_diet_habits, name='view_diet_habits'),
    path('view-physical-activities/', views.view_physical_activities, name='view_physical_activities'),
    path('add-diet-habit/', views.add_diet_habit, name='add_diet_habit'),
    path('add-physical-activity/', views.add_physical_activity, name='add_physical_activity'),
    path('friends/requests/send/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('friends/requests/accept/<int:user_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('public-records/', views.public_sleep_records, name='public_sleep_records'),
    path('friends-records/', views.friends_sleep_records, name='friends_sleep_records'),
    path('friends/handle/<int:friendship_id>/<str:action>/', views.handle_friend_request, name='handle_friend_request'),
    path('friends/', views.friends_list, name='friends_list'),
    path('friends/requests/', views.friend_requests, name='friend_requests'),
    path('friends/add/', views.send_friend_request, name='send_friend_request'),
    path('users/', views.users_list, name='users_list'),  # Добавляем URL для списка пользователей
    path('friends/add/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('friends/accept/<int:user_id>/', views.accept_friend_request, name='accept_friend_request'),

]
