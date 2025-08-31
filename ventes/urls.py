from django.urls import path
from . import views

app_name = 'ventes'

urlpatterns = [
    # Ventes
    path('ventes/', views.vente_list, name='vente_list'),
    path('ventes/nouvelle/', views.vente_create, name='vente_create'),
    path('ventes/export/', views.vente_export_excel, name='vente_export'),
    
    # Clients
    path('clients/', views.client_list, name='client_list'),
    path('clients/nouveau/', views.client_create, name='client_create'),
    path('clients/export/', views.client_export_excel, name='client_export'),
    
    # Statistiques
    path('statistiques/', views.statistiques_ventes, name='statistiques'),
]
