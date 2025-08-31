from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F, Q
from datetime import datetime, timedelta
from django.utils import timezone
import json
from ventes.models import Vente
from fournisseurs.models import Fournisseur, Livraison, Produit
from credits.models import CreditClient
from stocks.models import StockActuel


@login_required
def dashboard(request):
    """
    Vue principale du tableau de bord avec les statistiques générales
    """
    # Période de filtrage
    today = timezone.now().date()
    date_fin_str = request.GET.get('date_fin')
    date_debut_str = request.GET.get('date_debut')
    try:
        date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d').date() if date_fin_str else today
    except ValueError:
        date_fin = today
    try:
        date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date() if date_debut_str else (date_fin - timedelta(days=6))
    except ValueError:
        date_debut = date_fin - timedelta(days=6)

    # Ventes sur la période
    ventes_qs = Vente.objects.filter(date__range=(date_debut, date_fin))
    montant_ventes_periode = ventes_qs.aggregate(total=Sum('total_vente'))['total'] or 0

    # Ventes par jour (labels + data)
    # Génère la liste des dates dans l'intervalle
    nb_jours = (date_fin - date_debut).days + 1
    jours = [date_debut + timedelta(days=i) for i in range(nb_jours)]
    ventes_par_jour_dict = dict(
        ventes_qs.values('date').annotate(total=Sum('total_vente')).values_list('date', 'total')
    )
    labels = [j.strftime('%d/%m') for j in jours]
    data = [float(ventes_par_jour_dict.get(j, 0)) for j in jours]

    # Ventes du jour
    total_ventes_jour = Vente.objects.filter(date=today).aggregate(total=Sum('total_vente'))['total'] or 0

    # Produits actifs (ayant été vendus pendant la période)
    total_produits_actifs = (
        ventes_qs.values('produit_id').distinct().count()
    )

    # Crédits impayés (solde > 0)
    credits_impayes = CreditClient.objects.filter(solde_restant__gt=0).aggregate(total=Sum('solde_restant'))['total'] or 0

    # Stocks faibles (quantité <= seuil)
    stocks_faibles = (
        StockActuel.objects.select_related('produit', 'magasin')
        .filter(Q(quantite_actuelle__lte=0) | Q(quantite_actuelle__gt=0, quantite_actuelle__lte=F('seuil_alerte')))
        .order_by('magasin__nom', 'produit__nom')[:10]
    )

    # Dernières ventes
    dernieres_ventes = Vente.objects.select_related('client').order_by('-date', '-date_creation')[:10]

    context = {
        'title': 'Tableau de bord',
        'current_date': today,
        'date_debut': date_debut,
        'date_fin': date_fin,
        'total_ventes_jour': total_ventes_jour,
        'total_produits_actifs': total_produits_actifs,
        'credits_impayes': credits_impayes,
        'dernieres_ventes': dernieres_ventes,
        'stocks_faibles': stocks_faibles,
        'montant_ventes_periode': float(montant_ventes_periode),
        'ventes_labels_json': json.dumps(labels),
        'ventes_data_json': json.dumps(data),
    }

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
