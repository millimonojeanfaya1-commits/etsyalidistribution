from django.urls import path
from . import views

app_name = 'charges'

urlpatterns = [
    # Charges
    path('', views.charge_list, name='charge_list'),
    path('nouvelle/', views.charge_create, name='charge_create'),
    
    # Catégories
    path('categories/', views.categorie_list, name='categorie_list'),
    path('categories/nouvelle/', views.categorie_create, name='categorie_create'),
    
    # Budget
    path('budget/', views.budget_list, name='budget_list'),
    path('budget/nouveau/', views.budget_create, name='budget_create'),
    
    # Statistiques
    path('statistiques/', views.statistiques_charges, name='statistiques'),
]
