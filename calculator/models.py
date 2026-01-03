from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

from django.urls import reverse


class Material(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")

    class Meta:
        verbose_name = "Матеріал"
        verbose_name_plural = "Матеріали"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('material_detail', args=[str(self.id)])

    @property
    def total_weight(self):
        total = self.shipment_set.aggregate(models.Sum('crate__weight'))['crate__weight__sum']
        return total if total else 0


class Shipment(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name="Матеріал")
    shipment_date = models.DateField(default=date.today, verbose_name="Дата приходу")

    class Meta:
        verbose_name = "Відвантаження"
        verbose_name_plural = "Відвантаження"

    def __str__(self):
        return f"Відвантаження {self.material.name} від {self.shipment_date}"

class Crate(models.Model):

    STATUS_CHOICES = (
        ('arrived', 'Прийшло'),
        ('done', 'Виконано'),
        ('rejected', 'Заборонено'),
        ('returned', 'Повернуто'),
    )

    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, verbose_name="Відвантаження")
    status = models.CharField(max_length=50, verbose_name="Статус", choices=STATUS_CHOICES, default='arrived')
    weight = models.FloatField(verbose_name="Вага ящика (кг)")
    manufacture_date = models.DateField(default=date.today, verbose_name="Дата виготовлення")


    class Meta:
        verbose_name = "Ящик"
        verbose_name_plural = "Ящики"

    def __str__(self):
        return f"Ящик {self.id} - {self.shipment.material.name}"