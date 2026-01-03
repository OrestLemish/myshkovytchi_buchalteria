from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class CustomUser(AbstractUser):
    target_calories = models.PositiveIntegerField(default=0, verbose_name="Цільові калорії")
    target_proteins = models.FloatField(default=0, verbose_name="Цільові білки (г)")
    target_fats = models.FloatField(default=0, verbose_name="Цільові жири (г)")
    target_carbs = models.FloatField(default=0, verbose_name="Цільові вуглеводи (г)")


class DailyRecord(models.Model):
    """Model for tracking daily nutritional information"""
    date = models.DateField(verbose_name="Дата", default=date.today)
    user = models.ForeignKey(to='calculator.CustomUser', on_delete=models.CASCADE, related_name='daily_records', verbose_name="Користувач")

    # Computed fields for actual consumption

    def save(self, *args, **kwargs):
        # Get user from kwargs if provided (used when calling from views)
        current_user = kwargs.pop('current_user', None)
        if current_user and not self.user_id:
            self.user = current_user
        super().save(*args, **kwargs)


    @property
    def nutrition_data(self):
        # Calculate actual values once to avoid repeated queries
        total_calories = sum(meal.calories for meal in self.meals.all())
        total_proteins = round(sum(meal.proteins for meal in self.meals.all()), 2)
        total_fats = round(sum(meal.fats for meal in self.meals.all()), 2)
        total_carbs = round(sum(meal.carbs for meal in self.meals.all()), 2)

        # Get target values
        target_calories = self.user.target_calories
        target_proteins = round(self.user.target_proteins, 2)
        target_fats = round(self.user.target_fats, 2)
        target_carbs = round(self.user.target_carbs, 2)

        # Calculate percentages (avoiding division by zero)
        percentage_calories = round((total_calories / target_calories * 100) if target_calories > 0 else 0, 2)
        percentage_proteins = round((total_proteins / target_proteins * 100) if target_proteins > 0 else 0, 2)
        percentage_fats = round((total_fats / target_fats * 100) if target_fats > 0 else 0, 2)
        percentage_carbs = round((total_carbs / target_carbs * 100) if target_carbs > 0 else 0, 2)

        return {
            'target': {
                'calories': target_calories,
                'proteins': target_proteins,
                'fats': target_fats,
                'carbs': target_carbs,
            },
            'total': {
                'calories': total_calories,
                'proteins': total_proteins,
                'fats': total_fats,
                'carbs': total_carbs,
            },
            'remaining': {
                'calories': target_calories - total_calories,
                'proteins': round(target_proteins - total_proteins, 2),
                'fats': round(target_fats - total_fats, 2),
                'carbs': round(target_carbs - total_carbs, 2),
            },
            'percentage': {
                'calories': percentage_calories,
                'proteins': percentage_proteins,
                'fats': percentage_fats,
                'carbs': percentage_carbs,
            }
        }

    def __str__(self):
        return f"{self.user.username}'s record for {self.date}"

    class Meta:
        verbose_name = "Денний запис"
        verbose_name_plural = "Денні записи"
        unique_together = ['user', 'date']
        ordering = ['-date']


class Meal(models.Model):
    """Model for individual meals in a daily record"""
    MEAL_TYPES = [
        ('breakfast', 'Сніданок'),
        ('lunch', 'Обід'),
        ('dinner', 'Вечеря'),
        ('snack', 'Перекус'),
    ]

    daily_record = models.ForeignKey(DailyRecord, on_delete=models.CASCADE, related_name='meals', verbose_name="Денний запис")
    name = models.CharField(max_length=100, verbose_name="Назва")
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES, verbose_name="Тип прийому їжі", blank=True, null=True)
    time = models.TimeField(verbose_name="Час", blank=True, null=True)

    # Nutritional information
    calories = models.PositiveIntegerField(verbose_name="Калорії")
    proteins = models.FloatField(verbose_name="Білки (г)")
    fats = models.FloatField(verbose_name="Жири (г)")
    carbs = models.FloatField(verbose_name="Вуглеводи (г)")


    def __str__(self):
        return f"{self.name} ({self.get_meal_type_display()}) - {self.daily_record.date}"

    class Meta:
        verbose_name = "Прийом їжі"
        verbose_name_plural = "Прийоми їжі"
        ordering = ['time']
