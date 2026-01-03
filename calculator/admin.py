from django.contrib import admin
from django.utils.html import format_html

from .models import DailyRecord, Meal, CustomUser


class MealInline(admin.TabularInline):
    model = Meal
    extra = 1
    fields = ['name', 'meal_type', 'time', 'calories', 'proteins', 'fats', 'carbs']


@admin.register(DailyRecord)
class DailyRecordAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'total_calories']
    list_filter = ['date', 'user']
    search_fields = ['user__username']
    date_hierarchy = 'date'
    inlines = [MealInline]
    readonly_fields = [
        'calories_info',
        'proteins_info',
        'fats_info',
        'carbs_info',
        'meal_distribution_info',
    ]

    fieldsets = (
        ('Основна інформація', {
            'fields': ('date', 'user')
        }),
        ('Поживна інформація (розраховано автоматично)', {
            'fields': (
                'calories_info',
                'proteins_info',
                'fats_info',
                'carbs_info',
                'meal_distribution_info',
            ),
        }),
    )

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     # if request.user.is_superuser:
    #     #     return qs
    #     return qs.filter(user=request.user)

    def total_calories(self, obj):
        return sum(meal.calories for meal in obj.meals.all())

    total_calories.short_description = "Загальні калорії"

    def get_color(self, percentage):
        if percentage >= 95:
            return "#F44336"  # Green
        elif percentage >= 75:
            return "#FFC107"  # Yellow
        else:
            return "#4CAF50"  # Red

    def calories_info(self, obj):
        data = obj.nutrition_data
        percentage = data['percentage']['calories']
        color = self.get_color(percentage)
        return format_html(
            "<b>Ціль:</b> {} | <b>Факт:</b> <span style='background-color: {}; padding: 2px 5px; border-radius: 3px;'>{} ({}%)</span> | <b>Залишилось:</b> {}",
            data['target']['calories'],
            color,
            data['total']['calories'],
            round(percentage, 1),
            data['remaining']['calories']
        )

    calories_info.short_description = "Калорії"

    def proteins_info(self, obj):
        data = obj.nutrition_data
        percentage = data['percentage']['proteins']
        color = self.get_color(percentage)
        return format_html(
            "<b>Ціль:</b> {} | <b>Факт:</b> <span style='background-color: {}; padding: 2px 5px; border-radius: 3px;'>{} ({}%)</span> | <b>Залишилось:</b> {}",
            data['target']['proteins'],
            color,
            data['total']['proteins'],
            round(percentage, 1),
            data['remaining']['proteins']
        )

    proteins_info.short_description = "Білки"

    def fats_info(self, obj):
        data = obj.nutrition_data
        percentage = data['percentage']['fats']
        color = self.get_color(percentage)
        return format_html(
            "<b>Ціль:</b> {} | <b>Факт:</b> <span style='background-color: {}; padding: 2px 5px; border-radius: 3px;'>{} ({}%)</span> | <b>Залишилось:</b> {}",
            data['target']['fats'],
            color,
            data['total']['fats'],
            round(percentage, 1),
            data['remaining']['fats']
        )

    fats_info.short_description = "Жири"

    def carbs_info(self, obj):
        data = obj.nutrition_data
        percentage = data['percentage']['carbs']
        color = self.get_color(percentage)
        return format_html(
            "<b>Ціль:</b> {} | <b>Факт:</b> <span style='background-color: {}; padding: 2px 5px; border-radius: 3px;'>{} ({}%)</span> | <b>Залишилось:</b> {}",
            data['target']['carbs'],
            color,
            data['total']['carbs'],
            round(percentage, 1),
            data['remaining']['carbs']
        )

    carbs_info.short_description = "Вуглеводи"

    def meal_distribution_info(self, obj):
        total_calories = obj.user.target_calories

        return format_html(
            "<b>Сніданок:</b> {}-{} | <b>Перекус:</b> {}-{} | <b>Обід:</b> {}-{} | <b>Перекус:</b> {}-{} | <b>Вечеря:</b> {}-{}",
            round(total_calories * 0.25, 2), round(total_calories * 0.30, 2),
            round(total_calories * 0.05, 2), round(total_calories * 0.10, 2),
            round(total_calories * 0.30, 2), round(total_calories * 0.35, 2),
            round(total_calories * 0.05, 2), round(total_calories * 0.10, 2),
            round(total_calories * 0.25, 2), round(total_calories * 0.30, 2)
        )

    meal_distribution_info.short_description = "Розподіл калорій за прийомами їжі"


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass
