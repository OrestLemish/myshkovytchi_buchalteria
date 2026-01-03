from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Sum, Avg, Count
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView

from .models import CustomUser, DailyRecord, Meal
from .forms import MealForm, DailyRecordForm, UserProfileForm, CustomUserCreationForm

@login_required
def dashboard(request):
    """
    Display the dashboard with today's nutritional information and recent records
    """
    today = date.today()

    # Get or create today's record
    today_record = DailyRecord.objects.filter(user=request.user, date=today).first()

    # Get recent records (excluding today)
    recent_records = DailyRecord.objects.filter(
        user=request.user
    ).exclude(date=today).order_by('-date')[:5]

    context = {
        'today_record': today_record,
        'recent_records': recent_records,
    }

    return render(request, 'calculator/dashboard.html', context)

class DailyRecordListView(LoginRequiredMixin, ListView):
    """
    Display a list of all daily records for the current user
    """
    model = DailyRecord
    template_name = 'calculator/daily_record_list.html'
    context_object_name = 'daily_records'
    paginate_by = 10

    def get_queryset(self):
        return DailyRecord.objects.filter(user=self.request.user).order_by('-date')

class DailyRecordDetailView(LoginRequiredMixin, DetailView):
    """
    Display detailed information about a specific daily record
    """
    model = DailyRecord
    template_name = 'calculator/daily_record_detail.html'
    context_object_name = 'daily_record'

    def get_queryset(self):
        return DailyRecord.objects.filter(user=self.request.user)

class DailyRecordCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new daily record
    """
    model = DailyRecord
    form_class = DailyRecordForm
    template_name = 'calculator/daily_record_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # Set the user to the current user
        form.instance.user = self.request.user

        # Check if a record already exists for this date
        existing_record = DailyRecord.objects.filter(
            user=self.request.user,
            date=form.cleaned_data['date']
        ).first()

        if existing_record:
            messages.error(self.request, f"Запис на {form.cleaned_data['date']} вже існує")
            return self.form_invalid(form)

        messages.success(self.request, f"Запис на {form.cleaned_data['date']} створено успішно")
        return super().form_valid(form)

@login_required
def add_meal(request, record_id):
    """
    Add a new meal to a daily record
    """
    daily_record = get_object_or_404(DailyRecord, id=record_id, user=request.user)

    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.daily_record = daily_record
            meal.save()
            messages.success(request, "Прийом їжі додано успішно")
            return redirect('daily_record_detail', pk=daily_record.id)
    else:
        form = MealForm()

    return render(request, 'calculator/meal_form.html', {
        'form': form,
        'daily_record': daily_record
    })

@login_required
def edit_meal(request, meal_id):
    """
    Edit an existing meal
    """
    meal = get_object_or_404(Meal, id=meal_id, daily_record__user=request.user)
    daily_record = meal.daily_record

    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            messages.success(request, "Прийом їжі оновлено успішно")
            return redirect('daily_record_detail', pk=daily_record.id)
    else:
        form = MealForm(instance=meal)

    return render(request, 'calculator/meal_form.html', {
        'form': form,
        'daily_record': daily_record
    })

class MealDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a meal
    """
    model = Meal

    def get_queryset(self):
        return Meal.objects.filter(daily_record__user=self.request.user)

    def get_success_url(self):
        return reverse('daily_record_detail', kwargs={'pk': self.object.daily_record.id})

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Прийом їжі видалено успішно")
        return super().delete(request, *args, **kwargs)

@login_required
def profile(request):
    """
    Display and update user profile
    """
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль оновлено успішно")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)

    # Calculate statistics
    total_records = DailyRecord.objects.filter(user=user).count()
    total_meals = Meal.objects.filter(daily_record__user=user).count()

    # Calculate average calories (if there are records)
    avg_calories = None
    if total_records > 0:
        avg_calories = Meal.objects.filter(
            daily_record__user=user
        ).aggregate(avg=Avg('calories'))['avg']
        if avg_calories:
            avg_calories = round(avg_calories)

    # Calculate streak (consecutive days with records)
    streak = 0
    if total_records > 0:
        current_date = date.today()
        while DailyRecord.objects.filter(user=user, date=current_date).exists():
            streak += 1
            current_date -= timedelta(days=1)

    context = {
        'form': form,
        'total_records': total_records,
        'total_meals': total_meals,
        'avg_calories': avg_calories,
        'streak': streak if streak > 0 else None
    }

    return render(request, 'calculator/profile.html', context)


class CustomLoginView(LoginView):
    """
    Custom login view
    """
    template_name = 'calculator/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, "Ви успішно увійшли в систему")
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """
    Custom logout view
    """
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Ви вийшли з системи")
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    """
    View for user registration
    """
    form_class = CustomUserCreationForm
    template_name = 'calculator/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after registration
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, "Реєстрація успішна! Ласкаво просимо до FoodCalc.")
        return response

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)


class CustomPasswordChangeView(PasswordChangeView):
    """
    Custom password change view
    """
    template_name = 'calculator/password_change.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "Ваш пароль було успішно змінено")
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view
    """
    template_name = 'calculator/password_reset.html'
    email_template_name = 'calculator/password_reset_email.html'
    subject_template_name = 'calculator/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        messages.success(self.request, "Інструкції з відновлення пароля надіслано на вашу електронну пошту")
        return super().form_valid(form)
