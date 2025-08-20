from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from .models import AnalyseProfit, RapportProfitMensuel, ClassementProduit


@login_required
def analyse_list(request):
    """Liste des analyses de profit"""
    analyses = AnalyseProfit.objects.select_related('magasin', 'produit', 'commercial').all()
    
    context = {
        'title': 'Analyses de Profits',
        'analyses': analyses,
    }
    return render(request, 'profits/analyse_list.html', context)


@login_required
def analyse_create(request):
    """Créer une nouvelle analyse de profit"""
    context = {
        'title': 'Nouvelle Analyse de Profit',
    }
    return render(request, 'profits/analyse_form.html', context)


@login_required
def rapport_mensuel_list(request):
    """Liste des rapports mensuels"""
    rapports = RapportProfitMensuel.objects.select_related('magasin').all()
    
    context = {
        'title': 'Rapports Mensuels',
        'rapports': rapports,
    }
    return render(request, 'profits/rapport_mensuel_list.html', context)


@login_required
def generer_rapport_mensuel(request):
    """Générer un rapport mensuel"""
    context = {
        'title': 'Générer Rapport Mensuel',
    }
    return render(request, 'profits/generer_rapport.html', context)


@login_required
def classement_produits(request):
    """Classement des produits par rentabilité"""
    classements = ClassementProduit.objects.select_related('produit', 'magasin').all()
    
    context = {
        'title': 'Classement des Produits',
        'classements': classements,
    }
    return render(request, 'profits/classement_produits.html', context)


@login_required
def dashboard_profits(request):
    """Tableau de bord des profits"""
    total_analyses = AnalyseProfit.objects.count()
    profit_total = AnalyseProfit.objects.aggregate(Sum('profit_net'))['profit_net__sum'] or 0
    
    context = {
        'title': 'Tableau de Bord Profits',
        'total_analyses': total_analyses,
        'profit_total': profit_total,
    }
    return render(request, 'profits/dashboard_profits.html', context)


@login_required
def comparaisons_profits(request):
    """Comparaisons de profits"""
    context = {
        'title': 'Comparaisons de Profits',
    }
    return render(request, 'profits/comparaisons_profits.html', context)
