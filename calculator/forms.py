# calculator/forms.py
from django import forms
from .models import Shipment, Crate, Material


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                                           'placeholder': 'Назва матеріалу'}),
        }


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['shipment_date']
        widgets = {
            'shipment_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
        }


class CrateForm(forms.ModelForm):
    class Meta:
        model = Crate
        fields = ['status', 'weight', 'manufacture_date']
        widgets = {
            'status': forms.Select(
                attrs={'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'weight': forms.NumberInput(
                attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'manufacture_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
        }
