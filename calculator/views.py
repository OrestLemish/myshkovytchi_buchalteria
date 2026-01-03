# calculator/views.py
import json
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_http_methods, require_POST
from calculator.forms import ShipmentForm, CrateForm, MaterialForm
from calculator.models import Material, Shipment, Crate


@login_required
def index(request):
    # Додаємо анотацію для сортування за вагою
    materials = Material.objects.annotate(
        total_weight_val=Sum('shipment__crate__weight')
    ).all()
    context = {
        "materials": materials,
        "material_form": MaterialForm()  # Додаємо форму в контекст
    }
    return render(request, 'calculator/index.html', context)


class CustomLoginView(LoginView):
    template_name = 'calculator/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, "Ви успішно увійшли в систему")
        return super().form_valid(form)


# --- Material AJAX Views ---

@login_required
@require_POST
def material_add(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'errors': 'Invalid JSON'}, status=400)

    form = MaterialForm(data)
    if form.is_valid():
        material = form.save()
        return JsonResponse({
            'status': 'success',
            'material': {
                'id': material.id,
                'name': material.name,
                'url': material.get_absolute_url(),
            }
        })
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required
@require_http_methods(["POST"])
def material_edit(request, pk):
    material = get_object_or_404(Material, pk=pk)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'errors': 'Invalid JSON'}, status=400)

    form = MaterialForm(data, instance=material)
    if form.is_valid():
        material = form.save()
        return JsonResponse({
            'status': 'success',
            'material': {
                'id': material.id,
                'name': material.name,
            }
        })
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required
@require_http_methods(["DELETE"])
def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)
    material.delete()
    return JsonResponse({'status': 'success', 'message': 'Матеріал видалено.'})


# --- Existing Views ---

@login_required
def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)
    context = {
        "material": material,
        "shipment_form": ShipmentForm(),
        "crate_form": CrateForm(),
    }
    return render(request, 'calculator/material_detail.html', context)


@login_required
@require_POST
def shipment_add(request, material_id):
    material = get_object_or_404(Material, pk=material_id)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'errors': 'Invalid JSON'}, status=400)

    form = ShipmentForm(data)
    if form.is_valid():
        shipment = form.save(commit=False)
        shipment.material = material
        shipment.save()
        return JsonResponse({
            'status': 'success',
            'shipment': {
                'id': shipment.id,
                'shipment_date': shipment.shipment_date.strftime('%Y-%m-%d'),
                'edit_url': reverse('shipment_edit', args=[shipment.id]),
                'delete_url': reverse('shipment_delete', args=[shipment.id]),
                'add_crate_url': reverse('crate_add', args=[shipment.id]),
            }
        })
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required
@require_http_methods(["POST"])
def shipment_edit(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    data = json.loads(request.body)
    form = ShipmentForm(data, instance=shipment)
    if form.is_valid():
        shipment = form.save()
        return JsonResponse({
            'status': 'success',
            'shipment': {
                'id': shipment.id,
                'shipment_date': shipment.shipment_date.strftime('%Y-%m-%d'),
            }
        })
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required
@require_http_methods(["DELETE"])
def shipment_delete(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    shipment.delete()
    return JsonResponse({'status': 'success', 'message': 'Відвантаження видалено.'})


@login_required
@require_POST
def crate_add(request, shipment_id):
    shipment = get_object_or_404(Shipment, pk=shipment_id)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'errors': 'Invalid JSON'}, status=400)

    form = CrateForm(data)
    if form.is_valid():
        crate = form.save(commit=False)
        crate.shipment = shipment
        crate.save()
        return JsonResponse({
            'status': 'success',
            'crate': {
                'id': crate.id,
                'status': crate.status,
                'status_display': crate.get_status_display(),
                'weight': crate.weight,
                'manufacture_date': crate.manufacture_date.strftime('%Y-%m-%d'),
                'edit_url': reverse('crate_edit', args=[crate.id]),
                'delete_url': reverse('crate_delete', args=[crate.id]),
            }
        })
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required
@require_http_methods(["POST"])
def crate_edit(request, pk):
    crate = get_object_or_404(Crate, pk=pk)
    data = json.loads(request.body)
    form = CrateForm(data, instance=crate)
    if form.is_valid():
        crate = form.save()
        return JsonResponse({
            'status': 'success',
            'crate': {
                'id': crate.id,
                'status': crate.status,
                'status_display': crate.get_status_display(),
                'weight': crate.weight,
                'manufacture_date': crate.manufacture_date.strftime('%Y-%m-%d'),
            }
        })
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required
@require_http_methods(["DELETE"])
def crate_delete(request, pk):
    crate = get_object_or_404(Crate, pk=pk)
    crate.delete()
    return JsonResponse({'status': 'success', 'message': 'Ящик видалено.'})
