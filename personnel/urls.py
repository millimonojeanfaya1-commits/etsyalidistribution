from django.urls import path
from . import views

app_name = 'personnel'

urlpatterns = [
    # Employés
    path('', views.employe_list, name='employe_list'),
    path('nouveau/', views.employe_create, name='employe_create'),
    
    # Paies
    path('paies/', views.paie_list, name='paie_list'),
    path('paies/nouvelle/', views.paie_create, name='paie_create'),
    
    # Congés
    path('conges/', views.conge_list, name='conge_list'),
    
    # Statistiques
    path('statistiques/', views.statistiques_personnel, name='statistiques'),
]
