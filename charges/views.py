from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.core.paginator import Paginator
from .models import CategorieCharge, Charge, BudgetAnnuel


@login_required
def charge_list(request):
    """Liste des charges"""
    charges = Charge.objects.select_related('categorie').all()

    # Statistiques rapides pour l'en-tête
    now = timezone.now()
    total_charges = charges.aggregate(total=Sum('montant'))['total'] or 0
    charges_mois = charges.filter(date__year=now.year, date__month=now.month).aggregate(total=Sum('montant'))['total'] or 0
    charges_fixes = charges.filter(categorie__type_charge='fixe').aggregate(total=Sum('montant'))['total'] or 0
    charges_variables = charges.filter(categorie__type_charge='variable').aggregate(total=Sum('montant'))['total'] or 0
    
    context = {
        'title': 'Gestion des Charges',
        'charges': charges,
        'total_charges': total_charges,
        'charges_mois': charges_mois,
        'charges_fixes': charges_fixes,
        'charges_variables': charges_variables,
    }
    return render(request, 'charges/charge_list.html', context)


@login_required
def charge_create(request):
    """Créer une nouvelle charge"""
    from .forms import ChargeForm

    if request.method == 'POST':
        form = ChargeForm(request.POST)
        if form.is_valid():
            charge = form.save()
            messages.success(request, f"Charge {charge.numero} créée avec succès.")
            return redirect('charges:charge_list')
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = ChargeForm()

    context = {
        'title': 'Nouvelle Charge',
        'form': form,
    }
    return render(request, 'charges/charge_form.html', context)


@login_required
def categorie_list(request):
    """Liste des catégories de charges"""
    categories = CategorieCharge.objects.all()
    
    context = {
        'title': 'Catégories de Charges',
        'categories': categories,
    }
    return render(request, 'charges/categorie_list.html', context)


@login_required
def categorie_create(request):
    """Créer une nouvelle catégorie"""
    context = {
        'title': 'Nouvelle Catégorie',
    }
    return render(request, 'charges/categorie_form.html', context)


@login_required
def budget_list(request):
    """Liste des budgets"""
    budgets = BudgetAnnuel.objects.select_related('categorie').all()
    
    context = {
        'title': 'Budgets Annuels',
        'budgets': budgets,
    }
    return render(request, 'charges/budget_list.html', context)


@login_required
def budget_create(request):
    """Créer un nouveau budget"""
    context = {
        'title': 'Nouveau Budget',
    }
    return render(request, 'charges/budget_form.html', context)


@login_required
def statistiques_charges(request):
    """Statistiques des charges"""
    total_charges = Charge.objects.aggregate(Sum('montant'))['montant__sum'] or 0
    charges_fixes = Charge.objects.filter(categorie__type_charge='fixe').aggregate(
        Sum('montant')
    )['montant__sum'] or 0
    charges_variables = Charge.objects.filter(categorie__type_charge='variable').aggregate(
        Sum('montant')
    )['montant__sum'] or 0
    
    context = {
        'title': 'Statistiques Charges',
        'total_charges': total_charges,
        'charges_fixes': charges_fixes,
        'charges_variables': charges_variables,
    }
    return render(request, 'charges/statistiques.html', context)
