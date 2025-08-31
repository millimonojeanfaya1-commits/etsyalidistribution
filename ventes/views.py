from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Magasin, Client, Vente, Commercial
from stocks.models import StockActuel
from .forms import MagasinForm, ClientForm, VenteForm
from datetime import datetime, date as dt_date
import re


@login_required
def vente_list(request):
    """
    Liste des ventes avec filtres
    """
    ventes = Vente.objects.select_related('magasin', 'client', 'produit').all()
    
    # Filtres
    magasin_id = request.GET.get('magasin')
    if magasin_id:
        ventes = ventes.filter(magasin_id=magasin_id)
    
    type_vente = request.GET.get('type_vente')
    if type_vente:
        ventes = ventes.filter(type_vente=type_vente)
    
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    if date_debut:
        ventes = ventes.filter(date__gte=date_debut)
    if date_fin:
        ventes = ventes.filter(date__lte=date_fin)
    
    # Pagination
    paginator = Paginator(ventes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistiques
    total_ventes = ventes.aggregate(Sum('total_vente'))['total_vente__sum'] or 0
    ventes_cash = ventes.filter(type_vente='cash').aggregate(Sum('total_vente'))['total_vente__sum'] or 0
    ventes_credit = ventes.filter(type_vente='credit').aggregate(Sum('total_vente'))['total_vente__sum'] or 0
    
    context = {
        'title': 'Liste des Ventes',
        'page_obj': page_obj,
        'magasins': Magasin.objects.all(),
        'total_ventes': total_ventes,
        'ventes_cash': ventes_cash,
        'ventes_credit': ventes_credit,
        'filters': {
            'magasin': magasin_id,
            'type_vente': type_vente,
            'date_debut': date_debut,
            'date_fin': date_fin,
        }
    }
    return render(request, 'ventes/vente_list.html', context)


@login_required
def vente_create(request):
    """
    Créer une nouvelle vente
    """
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            numero = request.POST.get('numero')
            date = request.POST.get('date')
            magasin_id = request.POST.get('magasin')
            client_id = request.POST.get('client')
            produit_id = request.POST.get('produit')
            quantite_vendue = request.POST.get('quantite_vendue')
            prix_unitaire = request.POST.get('prix_unitaire')
            type_vente = request.POST.get('type_vente')
            
            # Validations serveur
            # Numéro: format VTE + chiffres (au moins 4)
            if not numero or not re.match(r'^VTE\d{4,}$', numero):
                messages.error(request, "Numéro invalide. Format attendu: VTE0001")
                raise ValueError('numero_invalide')

            # Date: valide et pas dans le futur
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            except Exception:
                messages.error(request, "Date invalide.")
                raise ValueError('date_invalide')
            if date_obj > dt_date.today():
                messages.error(request, "La date ne peut pas être dans le futur.")
                raise ValueError('date_future')

            # Type de vente
            if type_vente not in {'cash', 'credit'}:
                messages.error(request, "Type de vente invalide.")
                raise ValueError('type_vente_invalide')

            # Quantité et prix
            try:
                quantite_val = float(quantite_vendue)
            except Exception:
                messages.error(request, "Quantité invalide.")
                raise ValueError('quantite_invalide')
            if quantite_val <= 0:
                messages.error(request, "La quantité doit être positive.")
                raise ValueError('quantite_non_positive')

            try:
                prix_val = float(prix_unitaire)
            except Exception:
                messages.error(request, "Prix unitaire invalide.")
                raise ValueError('prix_invalide')
            if prix_val <= 0:
                messages.error(request, "Le prix unitaire doit être positif.")
                raise ValueError('prix_non_positif')
            
            # Résoudre le magasin
            magasin = None
            if magasin_id:
                if magasin_id.startswith('new_'):
                    # Ancien flux: création temporaire
                    magasin = Magasin.objects.create(
                        nom="Nouveau Magasin",
                        adresse="Adresse à compléter",
                        responsable="À définir"
                    )
                elif magasin_id.isdigit():
                    magasin = get_object_or_404(Magasin, id=magasin_id)
                else:
                    # Valeur texte depuis la liste fixe (ex: "MAGASIN N°1")
                    magasin, _ = Magasin.objects.get_or_create(
                        nom=magasin_id,
                        defaults={'adresse': '', 'responsable': ''}
                    )
            
            client = None
            if client_id and client_id.startswith('new_client_'):
                # Créer un nouveau client (pour la démo, on utilise des valeurs par défaut)
                client = Client.objects.create(
                    nom="Nouveau Client",
                    prenom="",
                    telephone="",
                    email=""
                )
            else:
                client = get_object_or_404(Client, id=client_id) if client_id else None
            
            # Pour les produits, on doit importer le modèle depuis fournisseurs
            from fournisseurs.models import Produit
            produit = None
            if produit_id:
                if produit_id.startswith('new_product_'):
                    # Ancien flux: création temporaire
                    produit = Produit.objects.create(
                        nom="Nouveau Produit",
                        description="Produit créé depuis le formulaire de vente",
                        unite_mesure="pièce",
                        prix_vente_conseille=float(prix_unitaire) if prix_unitaire else 0
                    )
                elif produit_id.isdigit():
                    produit = get_object_or_404(Produit, id=produit_id)
                else:
                    # Valeur texte depuis la liste fixe (ex: "RGB", "PT 44", etc.)
                    produit, _ = Produit.objects.get_or_create(
                        nom=produit_id,
                        defaults={
                            'description': 'Créé automatiquement depuis la vente',
                            'unite_mesure': 'pièce',
                            'prix_vente_conseille': float(prix_unitaire) if prix_unitaire else 0
                        }
                    )
            
            # Validation: le produit doit exister dans le magasin (stock actuel)
            if magasin and produit:
                try:
                    exists = StockActuel.objects.filter(magasin=magasin, produit=produit).exists()
                except Exception:
                    exists = False
                if not exists:
                    messages.error(request, "Le produit sélectionné n'est pas disponible dans le magasin choisi.")
                    raise ValueError('produit_non_disponible_dans_magasin')

            # Créer la vente
            if magasin and client and produit:
                vente = Vente.objects.create(
                    numero=numero,
                    date=date_obj,
                    magasin=magasin,
                    client=client,
                    produit=produit,
                    quantite_vendue=quantite_val,
                    prix_unitaire=prix_val,
                    type_vente=type_vente
                )
                messages.success(request, f'Vente {numero} enregistrée avec succès!')
                return redirect('ventes:vente_list')
            else:
                messages.error(request, 'Erreur: Tous les champs obligatoires doivent être remplis.')
                
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'enregistrement: {str(e)}')
    
    # Préparer les données pour le template
    from fournisseurs.models import Produit
    context = {
        'title': 'Nouvelle Vente',
        'magasins': Magasin.objects.all(),
        'clients': Client.objects.all(),
        'produits': Produit.objects.all(),
        'today': '2025-08-15',  # Date du jour
    }
    return render(request, 'ventes/vente_form.html', context)


@login_required
def client_list(request):
    """
    Liste des clients
    """
    clients = Client.objects.all()
    
    # Recherche
    search = request.GET.get('search')
    if search:
        clients = clients.filter(
            Q(nom__icontains=search) | 
            Q(prenom__icontains=search) |
            Q(telephone__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Liste des Clients',
        'page_obj': page_obj,
        'search': search,
    }
    return render(request, 'ventes/client_list.html', context)


@login_required
def client_create(request):
    """
    Créer un nouveau client
    """
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client créé avec succès!')
            return redirect('ventes:client_list')
    else:
        form = ClientForm()
    
    context = {
        'title': 'Nouveau Client',
        'form': form,
    }
    return render(request, 'ventes/client_form.html', context)


@login_required
def statistiques_ventes(request):
    """
    Statistiques des ventes
    """
    from datetime import datetime, timedelta
    from django.utils import timezone
    from django.db.models import TruncMonth, TruncDay
    
    # Statistiques générales
    total_ventes = Vente.objects.aggregate(Sum('total_vente'))['total_vente__sum'] or 0
    ventes_cash = Vente.objects.filter(type_vente='cash').aggregate(Sum('total_vente'))['total_vente__sum'] or 0
    ventes_credit = Vente.objects.filter(type_vente='credit').aggregate(Sum('total_vente'))['total_vente__sum'] or 0
    
    # Ventes par magasin
    ventes_par_magasin = Magasin.objects.annotate(
        total_ventes=Sum('vente__total_vente'),
        nb_ventes=Count('vente')
    ).filter(total_ventes__isnull=False).order_by('-total_ventes')
    
    # Ventes mensuelles (derniers 12 mois)
    date_limite = timezone.now().date() - timedelta(days=365)
    ventes_mensuelles = Vente.objects.filter(date__gte=date_limite).annotate(
        mois=TruncMonth('date')
    ).values('mois').annotate(
        total=Sum('total_vente'),
        nb_ventes=Count('id')
    ).order_by('mois')
    
    # Ventes journalières (derniers 30 jours)
    date_limite_jour = timezone.now().date() - timedelta(days=30)
    ventes_journalieres = Vente.objects.filter(date__gte=date_limite_jour).annotate(
        jour=TruncDay('date')
    ).values('jour').annotate(
        total=Sum('total_vente'),
        nb_ventes=Count('id')
    ).order_by('jour')
    
    context = {
        'title': 'Statistiques des Ventes',
        'total_ventes': total_ventes,
        'ventes_cash': ventes_cash,
        'ventes_credit': ventes_credit,
        'ventes_par_magasin': ventes_par_magasin,
        'ventes_mensuelles': ventes_mensuelles,
        'ventes_journalieres': ventes_journalieres,
    }
    return render(request, 'ventes/statistiques.html', context)


@login_required
def client_export_excel(request):
    """Exporter la liste des clients (avec recherche/type) en Excel"""
    clients = Client.objects.all().order_by('nom', 'prenom')

    search = request.GET.get('search')
    if search:
        clients = clients.filter(
            Q(nom__icontains=search)
            | Q(prenom__icontains=search)
            | Q(telephone__icontains=search)
        )
    type_client = request.GET.get('type_client')
    if type_client in {'particulier', 'entreprise'}:
        clients = clients.filter(type_client=type_client)

    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'Clients'
    ws.append(['Nom', 'Prénom', 'Téléphone', 'Email', 'Type', 'Limite crédit', 'Crédit actuel'])
    for c in clients:
        ws.append([
            c.nom,
            c.prenom or '',
            c.telephone or '',
            c.email or '',
            c.type_client,
            float(c.limite_credit) if c.limite_credit is not None else 0,
            float(c.credit_actuel) if c.credit_actuel is not None else 0,
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="clients.xlsx"'
    wb.save(response)
    return response


@login_required
def vente_export_excel(request):
    """Exporter la liste des ventes (avec filtres) en Excel"""
    ventes = Vente.objects.select_related('magasin', 'client', 'produit').all().order_by('-date')

    magasin_id = request.GET.get('magasin')
    if magasin_id:
        ventes = ventes.filter(magasin_id=magasin_id)
    type_vente = request.GET.get('type_vente')
    if type_vente in {'cash', 'credit'}:
        ventes = ventes.filter(type_vente=type_vente)
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    if date_debut:
        ventes = ventes.filter(date__gte=date_debut)
    if date_fin:
        ventes = ventes.filter(date__lte=date_fin)

    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'Ventes'
    ws.append(['N° Vente', 'Date', 'Magasin', 'Client', 'Produit', 'Quantité', 'Unité', 'Type', 'Prix unitaire', 'Total'])
    for v in ventes:
        ws.append([
            v.numero,
            v.date.strftime('%d/%m/%Y') if v.date else '',
            v.magasin.nom if v.magasin else '',
            str(v.client) if v.client else '',
            v.produit.nom if v.produit else '',
            float(v.quantite_vendue) if v.quantite_vendue is not None else 0,
            v.produit.unite_mesure if v.produit else '',
            v.type_vente,
            float(v.prix_unitaire) if v.prix_unitaire is not None else 0,
            float(v.total_vente) if getattr(v, 'total_vente', None) is not None else (float(v.quantite_vendue or 0) * float(v.prix_unitaire or 0)),
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="ventes.xlsx"'
    wb.save(response)
    return response
