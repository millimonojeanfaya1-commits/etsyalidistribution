from django.contrib import admin
from .models import CreditClient, Paiement


class PaiementInline(admin.TabularInline):
    model = Paiement
    extra = 1
    readonly_fields = ['date_creation']


@admin.register(CreditClient)
class CreditClientAdmin(admin.ModelAdmin):
    list_display = ['numero', 'date', 'client', 'magasin', 'produit', 
                   'montant_total', 'montant_paye', 'solde_restant', 'est_solde']
    list_filter = ['date', 'magasin', 'client', 'produit']
    search_fields = ['numero', 'client__nom', 'client__prenom', 'produit__nom']
    ordering = ['-date']
    readonly_fields = ['montant_total', 'solde_restant', 'date_creation', 'date_modification']
    inlines = [PaiementInline]
    
    def est_solde(self, obj):
        return obj.est_solde
    est_solde.boolean = True
    est_solde.short_description = 'Soldé'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('numero', 'date', 'client', 'magasin')
        }),
        ('Détails du crédit', {
            'fields': ('produit', 'quantite', 'prix_unitaire', 'montant_total')
        }),
        ('Paiements', {
            'fields': ('montant_paye', 'solde_restant')
        }),
        ('Observations', {
            'fields': ('observations',)
        }),
        ('Informations système', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['credit', 'date_paiement', 'montant', 'mode_paiement', 'reference']
    list_filter = ['date_paiement', 'mode_paiement']
    search_fields = ['credit__numero', 'credit__client__nom', 'reference']
    ordering = ['-date_paiement']
    readonly_fields = ['date_creation']
