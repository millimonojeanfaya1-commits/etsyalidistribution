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
        magasin_id = request.POST.get('magasin', '').strip()
        commercial_nom = request.POST.get('commercial', '').strip()
        produit_id = request.POST.get('produit', '').strip()
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

        if not magasin_id:
            errors.append("Le magasin est requis.")
        if not produit_id:
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
            # Résoudre les entités par ID
            try:
                magasin = Magasin.objects.get(id=magasin_id)
            except Magasin.DoesNotExist:
                messages.error(request, "Magasin introuvable.")
                magasin = None
            try:
                produit = Produit.objects.get(id=produit_id)
            except Produit.DoesNotExist:
                messages.error(request, "Produit introuvable.")
                produit = None
            commercial = None
            if commercial_nom:
                commercial, _ = Commercial.objects.get_or_create(nom=commercial_nom)

            # Validation: le produit doit exister dans le magasin (stock actuel)
            if magasin and produit:
                if not StockActuel.objects.filter(magasin=magasin, produit=produit).exists():
                    messages.error(request, "Le produit sélectionné n'est pas disponible dans le magasin choisi.")
                    return render(request, 'stocks/mouvement_form.html', {
                        'title': 'Nouveau Mouvement de Stock',
                        'magasins': Magasin.objects.all(),
                    })

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
        'magasins': Magasin.objects.all(),
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


@login_required
def stock_actuel_export_excel(request):
    """Exporter la liste du stock actuel en Excel (avec filtres)"""
    qs = StockActuel.objects.select_related('magasin', 'produit').all()

    # Filtres
    search = request.GET.get('search', '').strip()
    if search:
        qs = qs.filter(produit__nom__icontains=search)

    categorie = request.GET.get('categorie', '').strip()
    if categorie:
        # Utilise unite_mesure comme catégorie fonctionnelle
        qs = qs.filter(produit__unite_mesure=categorie)

    alerte = request.GET.get('alerte', '').strip()
    if alerte == 'critique':
        qs = qs.filter(quantite_actuelle__lte=0)
    elif alerte == 'faible':
        from django.db.models import F
        qs = qs.filter(quantite_actuelle__gt=0, quantite_actuelle__lte=F('seuil_alerte'))
    elif alerte == 'normal':
        from django.db.models import F
        qs = qs.filter(quantite_actuelle__gt=F('seuil_alerte'))

    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'Stock Actuel'
    ws.append([
        'Magasin', 'Produit', 'Unité', 'Quantité actuelle', 'Seuil alerte',
        'Prix moyen achat', 'Valeur stock', 'Dernière mise à jour'
    ])

    for s in qs.order_by('magasin__nom', 'produit__nom'):
        ws.append([
            s.magasin.nom if s.magasin else '',
            s.produit.nom if s.produit else '',
            getattr(s.produit, 'unite_mesure', '') or '',
            float(s.quantite_actuelle) if s.quantite_actuelle is not None else 0,
            float(s.seuil_alerte) if s.seuil_alerte is not None else 0,
            float(s.prix_moyen_achat) if s.prix_moyen_achat is not None else 0,
            float(s.valeur_stock) if s.valeur_stock is not None else 0,
            s.date_maj.strftime('%d/%m/%Y %H:%M') if s.date_maj else '',
        ])

    from django.http import HttpResponse
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="stock_actuel.xlsx"'
    wb.save(response)
    return response
