from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Employe, PaieSalaire, Conge
from .forms import EmployeForm


@login_required
def employe_list(request):
    """Liste des employés"""
    qs = Employe.objects.all().order_by('nom', 'prenoms')

    # Filtre statut
    status = request.GET.get('status', 'actifs')  # actifs | inactifs | all
    if status == 'actifs':
        qs = qs.filter(actif=True)
    elif status == 'inactifs':
        qs = qs.filter(actif=False)
    # 'all' -> pas de filtre

    # Recherche texte
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(
            Q(nom__icontains=q)
            | Q(prenoms__icontains=q)
            | Q(matricule__icontains=q)
            | Q(numero__icontains=q)
            | Q(fonction__icontains=q)
        )

    # Pagination
    page_size = 10
    paginator = Paginator(qs, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Stats simples
    total_employes = Employe.objects.count()
    employes_actifs = Employe.objects.filter(actif=True).count()

    context = {
        'title': 'Personnel',
        'employes': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'q': q,
        'status': status,
        'total_employes': total_employes,
        'employes_actifs': employes_actifs,
    }
    return render(request, 'personnel/employe_list.html', context)


@login_required
def employe_create(request):
    """Créer un nouvel employé"""
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            employe = form.save()
            messages.success(request, f"Employé {employe.nom_complet} créé avec succès.")
            return redirect('personnel:employe_list')
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = EmployeForm()

    context = {
        'title': 'Nouvel Employé',
        'form': form,
    }
    return render(request, 'personnel/employe_form.html', context)


@login_required
def employe_detail(request, pk):
    """Détails d'un employé"""
    employe = get_object_or_404(Employe, pk=pk)
    context = {
        'title': f"Employé · {employe.nom_complet}",
        'employe': employe,
    }
    return render(request, 'personnel/employe_detail.html', context)


@login_required
def employe_update(request, pk):
    """Modifier un employé"""
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            employe = form.save()
            messages.success(request, f"Employé {employe.nom_complet} modifié avec succès.")
            return redirect('personnel:employe_detail', pk=employe.pk)
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = EmployeForm(instance=employe)

    context = {
        'title': f"Modifier · {employe.nom_complet}",
        'form': form,
        'employe': employe,
    }
    return render(request, 'personnel/employe_form.html', context)


@login_required
def employe_delete(request, pk):
    """Désactiver (soft delete) un employé"""
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        employe.actif = False
        employe.save(update_fields=['actif'])
        messages.success(request, f"Employé {employe.nom_complet} désactivé.")
        return redirect('personnel:employe_list')

    context = {
        'title': f"Désactiver · {employe.nom_complet}",
        'employe': employe,
    }
    return render(request, 'personnel/employe_confirm_delete.html', context)


@login_required
def employe_activate(request, pk):
    """Réactiver un employé inactif"""
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        employe.actif = True
        employe.save(update_fields=['actif'])
        messages.success(request, f"Employé {employe.nom_complet} réactivé.")
        return redirect('personnel:employe_detail', pk=employe.pk)

    context = {
        'title': f"Réactiver · {employe.nom_complet}",
        'employe': employe,
    }
    return render(request, 'personnel/employe_confirm_activate.html', context)


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
    from .forms import PaieSalaireForm

    if request.method == 'POST':
        form = PaieSalaireForm(request.POST)
        if form.is_valid():
            paie = form.save()
            messages.success(request, f"Paie enregistrée pour {paie.employe.nom_complet} – {paie.get_mois_display()} {paie.annee}.")
            return redirect('personnel:paie_list')
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = PaieSalaireForm()

    context = {
        'title': 'Nouvelle Paie',
        'form': form,
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


@login_required
def employe_export_excel(request):
    """Exporter la liste des employés (avec filtres/recherche) en Excel"""
    # Reprendre la même logique de filtre/recherche que employe_list
    qs = Employe.objects.all().order_by('nom', 'prenoms')

    status = request.GET.get('status', 'actifs')
    if status == 'actifs':
        qs = qs.filter(actif=True)
    elif status == 'inactifs':
        qs = qs.filter(actif=False)

    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(
            Q(nom__icontains=q)
            | Q(prenoms__icontains=q)
            | Q(matricule__icontains=q)
            | Q(numero__icontains=q)
            | Q(fonction__icontains=q)
        )

    # Génération Excel
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'Employés'

    headers = [
        'N° Employé', 'Matricule', 'Nom', 'Prénoms', 'Fonction',
        "Date d'embauche", 'Salaire de base', 'Prime performance', 'Actif',
        'Téléphone', 'Email'
    ]
    ws.append(headers)

    for e in qs:
        ws.append([
            e.numero,
            e.matricule,
            e.nom,
            e.prenoms,
            e.fonction,
            e.date_embauche.strftime('%d/%m/%Y') if e.date_embauche else '',
            float(e.salaire_base) if e.salaire_base is not None else 0,
            float(e.prime_performance) if e.prime_performance is not None else 0,
            'Oui' if e.actif else 'Non',
            e.telephone or '',
            e.email or '',
        ])

    # Réponse HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="employes.xlsx"'
    wb.save(response)
    return response
