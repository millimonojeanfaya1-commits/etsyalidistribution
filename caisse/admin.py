from django.contrib import admin
from .models import MouvementCaisse


@admin.register(MouvementCaisse)
class MouvementCaisseAdmin(admin.ModelAdmin):
    list_display = ("date", "montant_entree", "montant_sortie")
    list_filter = ("date",)
    search_fields = ("observations",)
