from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from django.utils import timezone
import re
from decimal import Decimal, InvalidOperation
from .models import MouvementStock, StockActuel, Inventaire
from ventes.models import Magasin, Commercial
from fournisseurs.models import Produit


@login_required
def mouvement_list(request):
    """Liste des mouvements de stock"""
    mouvements = MouvementStock.objects.select_related('magasin', 'produit', 'commercial').all()
    
    paginator = Paginator(mouvements, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Mouvements de Stock',
        'page_obj': page_obj,
    }
    return render(request, 'stocks/mouvement_list.html', context)


@login_required
def mouvement_create(request):
    """Créer un nouveau mouvement de stock"""
    if request.method == 'POST':
        numero = request.POST.get('numero', '').strip()
        date_str = request.POST.get('date')
        magasin_nom = request.POST.get('magasin', '').strip()
        commercial_nom = request.POST.get('commercial', '').strip()
        produit_nom = request.POST.get('produit', '').strip()
        stock_initial = request.POST.get('stock_initial', '0').strip()
        stock_vendu = request.POST.get('stock_vendu', '0').strip()
        montant_ventes = request.POST.get('montant_ventes', '0').strip()
        observations = request.POST.get('observations', '').strip()

        # Validations
        errors = []
        if not re.match(r'^STK\d{4,}$', numero):
            errors.append("Le numéro doit respecter le format STK0001.")

        # Date
        try:
            from datetime import date as _date
            date_val = _date.fromisoformat(date_str)
            if date_val > timezone.now().date():
                errors.append("La date ne peut pas être dans le futur.")
        except Exception:
            errors.append("Date invalide.")

        if not magasin_nom:
            errors.append("Le magasin est requis.")
        if not produit_nom:
            errors.append("Le produit est requis.")

        # Numeriques
        def to_decimal(val, field):
            try:
                d = Decimal(val)
            except (InvalidOperation, TypeError):
                errors.append(f"Valeur invalide pour {field}.")
                return Decimal('0')
            if d < 0:
                errors.append(f"{field} ne peut pas être négatif.")
            return d

        si = to_decimal(stock_initial, 'Stock initial')
        sv = to_decimal(stock_vendu, 'Stock vendu')
        mv = to_decimal(montant_ventes, 'Montant des ventes')

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            # get_or_create entités
            magasin, _ = Magasin.objects.get_or_create(nom=magasin_nom)
            produit, _ = Produit.objects.get_or_create(nom=produit_nom)
            commercial = None
            if commercial_nom:
                commercial, _ = Commercial.objects.get_or_create(nom=commercial_nom)

            try:
                mouvement = MouvementStock.objects.create(
                    numero=numero,
                    date=date_val,
                    magasin=magasin,
                    commercial=commercial,
                    produit=produit,
                    stock_initial=si,
                    stock_vendu=sv,
                    montant_ventes=mv,
                    observations=observations or None,
                )
                messages.success(request, "Mouvement de stock enregistré avec succès.")
                return redirect('stocks:mouvement_list')
            except Exception as ex:
                messages.error(request, f"Erreur lors de l'enregistrement: {ex}")

    context = {
        'title': 'Nouveau Mouvement de Stock',
    }
    return render(request, 'stocks/mouvement_form.html', context)


@login_required
def stock_actuel_list(request):
    """Liste des stocks actuels"""
    stocks = StockActuel.objects.select_related('magasin', 'produit').all()
    
    context = {
        'title': 'Stocks Actuels',
        'stocks': stocks,
    }
    return render(request, 'stocks/stock_actuel_list.html', context)


@login_required
def alertes_stock(request):
    """Alertes de stock"""
    stocks_faibles = StockActuel.objects.filter(
        quantite_actuelle__lte=models.F('seuil_alerte')
    ).select_related('magasin', 'produit')
    
    context = {
        'title': 'Alertes de Stock',
        'stocks_faibles': stocks_faibles,
    }
    return render(request, 'stocks/alertes_stock.html', context)


@login_required
def inventaire_list(request):
    """Liste des inventaires"""
    inventaires = Inventaire.objects.select_related('magasin').all()
    
    context = {
        'title': 'Inventaires',
        'inventaires': inventaires,
    }
    return render(request, 'stocks/inventaire_list.html', context)


@login_required
def inventaire_create(request):
    """Créer un nouvel inventaire"""
    context = {
        'title': 'Nouvel Inventaire',
    }
    return render(request, 'stocks/inventaire_form.html', context)


@login_required
def statistiques_stocks(request):
    """Statistiques des stocks"""
    context = {
        'title': 'Statistiques Stocks',
    }
    return render(request, 'stocks/statistiques.html', context)
