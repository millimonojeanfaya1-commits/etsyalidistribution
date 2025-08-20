from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.utils import timezone


@login_required
def dashboard(request):
    """
    Vue principale du tableau de bord avec les statistiques générales
    """
    context = {
        'title': 'Tableau de bord',
        'current_date': timezone.now().date(),
    }
    
    # Ici nous ajouterons les statistiques une fois les modèles créés
    # context['total_ventes_jour'] = Vente.objects.filter(date=timezone.now().date()).aggregate(Sum('total_vente'))['total_vente__sum'] or 0
    # context['total_fournisseurs'] = Fournisseur.objects.count()
    # context['stock_alerts'] = Stock.objects.filter(stock_final__lt=10).count()
    
    return render(request, 'core/dashboard.html', context)


def login_view(request):
    """
    Vue de connexion personnalisée
    """
    return render(request, 'registration/login.html')


@login_required
def profile_view(request):
    """
    Vue du profil utilisateur
    """
    context = {
        'title': 'Mon Profil',
        'user': request.user,
    }
    return render(request, 'core/profile.html', context)
