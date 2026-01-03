# calculator/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.index, name='index'),

    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),

    # Material (Page & AJAX)
    path('material/add/', views.material_add, name='material_add'),
    path('material/<int:pk>/', views.material_detail, name='material_detail'),
    path('material/<int:pk>/edit/', views.material_edit, name='material_edit'),
    path('material/<int:pk>/delete/', views.material_delete, name='material_delete'),

    # Shipment CRUD (AJAX)
    path('material/<int:material_id>/shipment/add/', views.shipment_add, name='shipment_add'),
    path('shipment/<int:pk>/edit/', views.shipment_edit, name='shipment_edit'),
    path('shipment/<int:pk>/delete/', views.shipment_delete, name='shipment_delete'),

    # Crate CRUD (AJAX)
    path('shipment/<int:shipment_id>/crate/add/', views.crate_add, name='crate_add'),
    path('crate/<int:pk>/edit/', views.crate_edit, name='crate_edit'),
    path('crate/<int:pk>/delete/', views.crate_delete, name='crate_delete'),
]
