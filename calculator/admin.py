from django.contrib import admin
from django.utils.html import format_html

from .models import Material, Shipment, Crate


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Crate)
class CrateAdmin(admin.ModelAdmin):
    pass

