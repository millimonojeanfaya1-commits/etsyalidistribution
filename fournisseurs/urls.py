from django.urls import path
from . import views

app_name = 'fournisseurs'

urlpatterns = [
    # Fournisseurs
    path('', views.fournisseur_list, name='fournisseur_list'),
    path('nouveau/', views.fournisseur_create, name='fournisseur_create'),
    path('<int:pk>/modifier/', views.fournisseur_edit, name='fournisseur_edit'),
    path('export/fournisseurs/', views.fournisseur_export_excel, name='fournisseur_export'),
    path('export/produits/', views.produit_export_excel, name='produit_export'),
    
    # Livraisons
    path('livraisons/', views.livraison_list, name='livraison_list'),
    path('livraisons/nouvelle/', views.livraison_create, name='livraison_create'),
    path('livraisons/export/', views.livraison_export_excel, name='livraison_export'),
    
    # Statistiques
    path('statistiques/', views.statistiques_fournisseurs, name='statistiques'),
]
