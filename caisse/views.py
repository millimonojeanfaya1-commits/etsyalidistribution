from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime
from .models import MouvementCaisse
from .forms import MouvementCaisseForm


def caisse_list(request):
    # Filtres de période
    date_debut_str = request.GET.get('date_debut')
    date_fin_str = request.GET.get('date_fin')
    qs = MouvementCaisse.objects.all()

    date_debut = None
    date_fin = None
    try:
        if date_debut_str:
            date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()
        if date_fin_str:
            date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, "Format de date invalide. Utilisez YYYY-MM-DD.")

    if date_debut and date_fin:
        qs = qs.filter(date__range=(date_debut, date_fin))
    elif date_debut:
        qs = qs.filter(date__gte=date_debut)
    elif date_fin:
        qs = qs.filter(date__lte=date_fin)

    total_entree = qs.aggregate(s=Sum('montant_entree'))['s'] or 0
    total_sortie = qs.aggregate(s=Sum('montant_sortie'))['s'] or 0
    solde = total_entree - total_sortie

    # Export CSV
    if request.GET.get('export') == 'csv':
        import csv
        response = HttpResponse(content_type='text/csv')
        filename = 'caisse_export.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow(['Date', 'Libellé', 'Montant entrée', 'Montant sortie', 'Observations'])
        for m in qs.order_by('date', 'id'):
            writer.writerow([m.date.isoformat(), m.libelle or '', f"{m.montant_entree}", f"{m.montant_sortie}", (m.observations or '').replace('\n', ' ')])
        return response

    # Résumés quotidiens et mensuels
    resume_jour_qs = (
        qs.values('date')
          .annotate(entree=Sum('montant_entree'), sortie=Sum('montant_sortie'))
          .order_by('-date')
    )
    resume_jour = []
    for r in resume_jour_qs:
        e = r.get('entree') or 0
        s = r.get('sortie') or 0
        r['solde'] = e - s
        resume_jour.append(r)

    resume_mois_qs = (
        qs.annotate(mois=TruncMonth('date'))
          .values('mois')
          .annotate(entree=Sum('montant_entree'), sortie=Sum('montant_sortie'))
          .order_by('-mois')
    )
    resume_mois = []
    for r in resume_mois_qs:
        e = r.get('entree') or 0
        s = r.get('sortie') or 0
        r['solde'] = e - s
        resume_mois.append(r)

    return render(request, 'caisse/mouvement_list.html', {
        'mouvements': qs.order_by('-date', '-id'),
        'total_entree': total_entree,
        'total_sortie': total_sortie,
        'solde': solde,
        'date_debut': date_debut,
        'date_fin': date_fin,
        'resume_jour': resume_jour,
        'resume_mois': resume_mois,
    })


def caisse_print(request):
    # même logique de filtre que la liste
    date_debut_str = request.GET.get('date_debut')
    date_fin_str = request.GET.get('date_fin')
    qs = MouvementCaisse.objects.all()

    date_debut = None
    date_fin = None
    try:
        if date_debut_str:
            date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()
        if date_fin_str:
            date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, "Format de date invalide. Utilisez YYYY-MM-DD.")

    if date_debut and date_fin:
        qs = qs.filter(date__range=(date_debut, date_fin))
    elif date_debut:
        qs = qs.filter(date__gte=date_debut)
    elif date_fin:
        qs = qs.filter(date__lte=date_fin)

    total_entree = qs.aggregate(s=Sum('montant_entree'))['s'] or 0
    total_sortie = qs.aggregate(s=Sum('montant_sortie'))['s'] or 0
    solde = total_entree - total_sortie

    resume_jour_qs = (
        qs.values('date')
          .annotate(entree=Sum('montant_entree'), sortie=Sum('montant_sortie'))
          .order_by('-date')
    )
    resume_jour = []
    for r in resume_jour_qs:
        e = r.get('entree') or 0
        s = r.get('sortie') or 0
        r['solde'] = e - s
        resume_jour.append(r)

    return render(request, 'caisse/mouvement_print.html', {
        'mouvements': qs.order_by('date', 'id'),
        'total_entree': total_entree,
        'total_sortie': total_sortie,
        'solde': solde,
        'date_debut': date_debut,
        'date_fin': date_fin,
        'resume_jour': resume_jour,
    })


def caisse_create(request):
    if request.method == 'POST':
        form = MouvementCaisseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mouvement de caisse enregistré avec succès.")
            return redirect(reverse('caisse:list'))
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = MouvementCaisseForm()
    return render(request, 'caisse/mouvement_form.html', {'form': form})
