from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from .models import Employe, PaieSalaire, Conge


@login_required
def employe_list(request):
    """Liste des employés"""
    employes = Employe.objects.filter(actif=True)
    
    context = {
        'title': 'Personnel',
        'employes': employes,
    }
    return render(request, 'personnel/employe_list.html', context)


@login_required
def employe_create(request):
    """Créer un nouvel employé"""
    context = {
        'title': 'Nouvel Employé',
    }
    return render(request, 'personnel/employe_form.html', context)


@login_required
def paie_list(request):
    """Liste des paies"""
    paies = PaieSalaire.objects.select_related('employe').all()
    
    context = {
        'title': 'Gestion des Paies',
        'paies': paies,
    }
    return render(request, 'personnel/paie_list.html', context)


@login_required
def paie_create(request):
    """Créer une nouvelle paie"""
    context = {
        'title': 'Nouvelle Paie',
    }
    return render(request, 'personnel/paie_form.html', context)


@login_required
def conge_list(request):
    """Liste des congés"""
    conges = Conge.objects.select_related('employe').all()
    
    context = {
        'title': 'Gestion des Congés',
        'conges': conges,
    }
    return render(request, 'personnel/conge_list.html', context)


@login_required
def statistiques_personnel(request):
    """Statistiques du personnel"""
    total_employes = Employe.objects.filter(actif=True).count()
    masse_salariale = Employe.objects.filter(actif=True).aggregate(
        total=Sum('salaire_base')
    )['total'] or 0
    
    context = {
        'title': 'Statistiques Personnel',
        'total_employes': total_employes,
        'masse_salariale': masse_salariale,
    }
    return render(request, 'personnel/statistiques.html', context)
