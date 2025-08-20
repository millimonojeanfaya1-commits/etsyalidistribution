from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from .models import CreditClient, Paiement


@login_required
def credit_list(request):
    """
    Liste des crédits clients avec filtres
    """
    credits = CreditClient.objects.select_related('client', 'magasin', 'produit').all()
    
    # Filtres
    statut = request.GET.get('statut')
    if statut == 'solde':
        credits = credits.filter(solde_restant__lte=0)
    elif statut == 'impaye':
        credits = credits.filter(solde_restant__gt=0)
    
    client_id = request.GET.get('client')
    if client_id:
        credits = credits.filter(client_id=client_id)
    
    # Pagination
    paginator = Paginator(credits, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistiques
    total_credits = credits.aggregate(Sum('montant_total'))['montant_total__sum'] or 0
    total_paye = credits.aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
    total_impaye = credits.aggregate(Sum('solde_restant'))['solde_restant__sum'] or 0
    
    context = {
        'title': 'Crédits Clients',
        'page_obj': page_obj,
        'total_credits': total_credits,
        'total_paye': total_paye,
        'total_impaye': total_impaye,
        'filters': {
            'statut': statut,
            'client': client_id,
        }
    }
    return render(request, 'credits/credit_list.html', context)


@login_required
def credit_create(request):
    """
    Créer un nouveau crédit
    """
    from .forms import CreditClientForm
    
    if request.method == 'POST':
        form = CreditClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crédit enregistré avec succès!')
            return redirect('credits:credit_list')
    else:
        form = CreditClientForm()
    
    context = {
        'title': 'Nouveau Crédit',
        'form': form,
    }
    return render(request, 'credits/credit_form.html', context)


@login_required
def credit_detail(request, pk):
    """
    Détail d'un crédit avec historique des paiements
    """
    credit = get_object_or_404(CreditClient, pk=pk)
    paiements = credit.paiements.all()
    
    context = {
        'title': f'Crédit {credit.numero}',
        'credit': credit,
        'paiements': paiements,
    }
    return render(request, 'credits/credit_detail.html', context)


@login_required
def paiement_create(request, credit_pk):
    """
    Enregistrer un paiement pour un crédit
    """
    from .forms import PaiementForm
    
    credit = get_object_or_404(CreditClient, pk=credit_pk)
    
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.credit = credit
            paiement.save()
            messages.success(request, 'Paiement enregistré avec succès!')
            return redirect('credits:credit_detail', pk=credit.pk)
    else:
        form = PaiementForm()
    
    context = {
        'title': f'Nouveau Paiement - {credit.numero}',
        'form': form,
        'credit': credit,
    }
    return render(request, 'credits/paiement_form.html', context)


@login_required
def statistiques_credits(request):
    """
    Statistiques des crédits et recouvrements
    """
    from django.db.models import Avg
    
    # Statistiques générales
    total_credits = CreditClient.objects.aggregate(Sum('montant_total'))['montant_total__sum'] or 0
    total_paye = CreditClient.objects.aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
    total_impaye = CreditClient.objects.aggregate(Sum('solde_restant'))['solde_restant__sum'] or 0
    
    taux_recouvrement_global = (total_paye / total_credits * 100) if total_credits > 0 else 0
    
    # Clients débiteurs
    clients_debiteurs = CreditClient.objects.filter(solde_restant__gt=0).values(
        'client__nom', 'client__prenom'
    ).annotate(
        total_du=Sum('solde_restant'),
        nb_credits=Count('id')
    ).order_by('-total_du')
    
    context = {
        'title': 'Statistiques Crédits',
        'total_credits': total_credits,
        'total_paye': total_paye,
        'total_impaye': total_impaye,
        'taux_recouvrement_global': taux_recouvrement_global,
        'clients_debiteurs': clients_debiteurs,
    }
    return render(request, 'credits/statistiques.html', context)
