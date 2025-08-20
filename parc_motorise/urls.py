from django.urls import path
from . import views

app_name = 'parc_motorise'

urlpatterns = [
    # Véhicules
    path('', views.vehicule_list, name='vehicule_list'),
    path('nouveau/', views.vehicule_create, name='vehicule_create'),
    
    # Consommations carburant
    path('consommations/', views.consommation_list, name='consommation_list'),
    path('consommations/nouvelle/', views.consommation_create, name='consommation_create'),
    
    # Maintenances
    path('maintenances/', views.maintenance_list, name='maintenance_list'),
    path('maintenances/nouvelle/', views.maintenance_create, name='maintenance_create'),
    
    # Statistiques
    path('statistiques/', views.statistiques_parc, name='statistiques'),
]
