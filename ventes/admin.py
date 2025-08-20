from django.contrib import admin
from .models import Magasin, Client, Vente, Commercial


@admin.register(Magasin)
class MagasinAdmin(admin.ModelAdmin):
    list_display = ['nom', 'responsable', 'telephone', 'date_creation']
    list_filter = ['date_creation']
    search_fields = ['nom', 'responsable', 'telephone']
    ordering = ['nom']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'telephone', 'email', 'date_creation']
    list_filter = ['date_creation']
    search_fields = ['nom', 'prenom', 'telephone', 'email']
    ordering = ['nom', 'prenom']


@admin.register(Commercial)
class CommercialAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'magasin', 'commission_pourcentage', 
                   'date_embauche', 'actif']
    list_filter = ['magasin', 'actif', 'date_embauche']
    search_fields = ['nom', 'prenom', 'telephone', 'email']
    ordering = ['nom', 'prenom']


@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'date', 'magasin', 'client', 'produit', 
                   'quantite_vendue', 'type_vente', 'prix_unitaire', 'total_vente']
    list_filter = ['date', 'magasin', 'type_vente', 'produit']
    search_fields = ['numero', 'client__nom', 'client__prenom', 'produit__nom']
    ordering = ['-date']
    readonly_fields = ['total_vente', 'date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('numero', 'date', 'magasin', 'client')
        }),
        ('Détails de la vente', {
            'fields': ('produit', 'quantite_vendue', 'prix_unitaire', 'total_vente', 'type_vente')
        }),
        ('Informations système', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
