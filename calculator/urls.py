from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Password management
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='calculator/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='calculator/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='calculator/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # Daily Records
    path('records/', views.DailyRecordListView.as_view(), name='daily_record_list'),
    path('records/<int:pk>/', views.DailyRecordDetailView.as_view(), name='daily_record_detail'),
    path('records/create/', views.DailyRecordCreateView.as_view(), name='create_daily_record'),
    
    # Meals
    path('records/<int:record_id>/add-meal/', views.add_meal, name='add_meal'),
    path('meals/<int:meal_id>/edit/', views.edit_meal, name='edit_meal'),
    path('meals/<int:pk>/delete/', views.MealDeleteView.as_view(), name='delete_meal'),
    
    # User Profile
    path('profile/', views.profile, name='profile'),
]