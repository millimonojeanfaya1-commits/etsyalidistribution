from django.urls import path
from . import views

app_name = 'caisse'

urlpatterns = [
    path('', views.caisse_list, name='list'),
    path('nouveau/', views.caisse_create, name='create'),
    path('imprimer/', views.caisse_print, name='print'),
]
