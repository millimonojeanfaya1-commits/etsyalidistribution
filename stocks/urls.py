from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    # Mouvements de stock
    path('', views.mouvement_list, name='mouvement_list'),
    path('nouveau/', views.mouvement_create, name='mouvement_create'),
    
    # Stock actuel
    path('actuel/', views.stock_actuel_list, name='stock_actuel_list'),
    path('alertes/', views.alertes_stock, name='alertes_stock'),
    path('actuel/export/', views.stock_actuel_export_excel, name='stock_actuel_export'),
    
    # Inventaires
    path('inventaires/', views.inventaire_list, name='inventaire_list'),
    path('inventaires/nouveau/', views.inventaire_create, name='inventaire_create'),
    
    # Statistiques
    path('statistiques/', views.statistiques_stocks, name='statistiques'),
]
