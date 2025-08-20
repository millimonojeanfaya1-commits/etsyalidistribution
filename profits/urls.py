from django.urls import path
from . import views

app_name = 'profits'

urlpatterns = [
    # Analyses de profit
    path('', views.analyse_list, name='analyse_list'),
    path('nouvelle/', views.analyse_create, name='analyse_create'),
    
    # Rapports mensuels
    path('rapports/', views.rapport_mensuel_list, name='rapport_mensuel_list'),
    path('rapports/generer/', views.generer_rapport_mensuel, name='generer_rapport_mensuel'),
    
    # Classements
    path('classements/', views.classement_produits, name='classement_produits'),
    
    # Statistiques et tableaux de bord
    path('dashboard/', views.dashboard_profits, name='dashboard_profits'),
    path('comparaisons/', views.comparaisons_profits, name='comparaisons_profits'),
]
