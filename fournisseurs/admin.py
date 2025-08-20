from django.contrib import admin
from .models import Fournisseur, Produit, Livraison


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'telephone', 'email', 'date_creation']
    list_filter = ['date_creation']
    search_fields = ['nom', 'telephone', 'email']
    ordering = ['nom']


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'unite_mesure', 'prix_vente_conseille', 'date_creation']
    list_filter = ['unite_mesure', 'date_creation']
    search_fields = ['nom', 'description']
    ordering = ['nom']


@admin.register(Livraison)
class LivraisonAdmin(admin.ModelAdmin):
    list_display = ['numero_enregistrement', 'date', 'fournisseur', 'produit', 
                   'quantite_livree', 'prix_achat_unitaire', 'montant_total_achat']
    list_filter = ['date', 'fournisseur', 'produit']
    search_fields = ['numero_enregistrement', 'fournisseur__nom', 'produit__nom']
    ordering = ['-date']
    readonly_fields = ['montant_total_achat', 'date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('numero_enregistrement', 'date', 'fournisseur', 'produit')
        }),
        ('Détails de la livraison', {
            'fields': ('quantite_livree', 'prix_achat_unitaire', 'montant_total_achat')
        }),
        ('Observations', {
            'fields': ('observations',)
        }),
        ('Informations système', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
