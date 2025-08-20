from django.urls import path
from . import views

app_name = 'ventes'

urlpatterns = [
    # Ventes
    path('', views.vente_list, name='vente_list'),
    path('nouvelle/', views.vente_create, name='vente_create'),
    
    # Clients
    path('clients/', views.client_list, name='client_list'),
    path('clients/nouveau/', views.client_create, name='client_create'),
    
    # Statistiques
    path('statistiques/', views.statistiques_ventes, name='statistiques'),
]
