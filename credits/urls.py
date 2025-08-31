from django.urls import path
from . import views

app_name = 'credits'

urlpatterns = [
    # Crédits
    path('', views.credit_list, name='credit_list'),
    path('nouveau/', views.credit_create, name='credit_create'),
    path('<int:pk>/detail/', views.credit_detail, name='credit_detail'),
    
    # Paiements
    path('<int:credit_pk>/paiement/', views.paiement_create, name='paiement_create'),
    # Export
    path('export/', views.credit_export_excel, name='credit_export'),
    
    # Statistiques
    path('statistiques/', views.statistiques_credits, name='statistiques'),

    # API JSON
    path('magasin/<int:magasin_id>/produits/', views.produits_par_magasin, name='produits_par_magasin'),
]
