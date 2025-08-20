from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from .models import Vehicule, ConsommationCarburant, MaintenanceVehicule


@login_required
def vehicule_list(request):
    """Liste des véhicules"""
    vehicules = Vehicule.objects.all()
    
    context = {
        'title': 'Parc Motorisé',
        'vehicules': vehicules,
    }
    return render(request, 'parc_motorise/vehicule_list.html', context)


@login_required
def vehicule_create(request):
    """Créer un nouveau véhicule"""
    context = {
        'title': 'Nouveau Véhicule',
    }
    return render(request, 'parc_motorise/vehicule_form.html', context)


@login_required
def consommation_list(request):
    """Liste des consommations de carburant"""
    consommations = ConsommationCarburant.objects.select_related('vehicule').all()
    
    context = {
        'title': 'Consommations Carburant',
        'consommations': consommations,
    }
    return render(request, 'parc_motorise/consommation_list.html', context)


@login_required
def consommation_create(request):
    """Créer une nouvelle consommation"""
    context = {
        'title': 'Nouvelle Consommation',
    }
    return render(request, 'parc_motorise/consommation_form.html', context)


@login_required
def maintenance_list(request):
    """Liste des maintenances"""
    maintenances = MaintenanceVehicule.objects.select_related('vehicule').all()
    
    context = {
        'title': 'Maintenances',
        'maintenances': maintenances,
    }
    return render(request, 'parc_motorise/maintenance_list.html', context)


@login_required
def maintenance_create(request):
    """Créer une nouvelle maintenance"""
    context = {
        'title': 'Nouvelle Maintenance',
    }
    return render(request, 'parc_motorise/maintenance_form.html', context)


@login_required
def statistiques_parc(request):
    """Statistiques du parc motorisé"""
    total_vehicules = Vehicule.objects.count()
    vehicules_actifs = Vehicule.objects.filter(statut='actif').count()
    
    context = {
        'title': 'Statistiques Parc Motorisé',
        'total_vehicules': total_vehicules,
        'vehicules_actifs': vehicules_actifs,
    }
    return render(request, 'parc_motorise/statistiques.html', context)
