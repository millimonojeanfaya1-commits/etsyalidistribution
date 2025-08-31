from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column
from .models import CreditClient, Paiement
from fournisseurs.models import Produit
from stocks.models import StockActuel
from datetime import date as dt_date
import re


class CreditClientForm(forms.ModelForm):
    """
    Formulaire pour créer un crédit client
    """
    class Meta:
        model = CreditClient
        fields = ['numero', 'date', 'client', 'magasin', 'produit', 
                 'quantite', 'prix_unitaire', 'observations']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'observations': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hints/attrs
        self.fields['numero'].widget.attrs.update({
            'placeholder': 'CRD0001',
            'pattern': r'^CRD\\d{4,}$',
            'title': 'Format attendu: CRD0001'
        })
        # Listes déroulantes pour client, magasin et produit
        if 'client' in self.fields:
            self.fields['client'].queryset = self.fields['client'].queryset.order_by('nom')
            self.fields['client'].empty_label = '— Sélectionner un client —'
            self.fields['client'].widget.attrs.update({'class': 'form-select'})
        if 'magasin' in self.fields:
            self.fields['magasin'].queryset = self.fields['magasin'].queryset.order_by('nom')
            self.fields['magasin'].empty_label = '— Sélectionner un magasin —'
            self.fields['magasin'].widget.attrs.update({'class': 'form-select'})
        if 'produit' in self.fields:
            # Par défaut, pas de produits tant qu'un magasin n'est pas choisi
            produits_qs = Produit.objects.none()
            # Si un magasin est fourni (POST/GET), filtrer les produits disponibles dans ce magasin
            magasin_id = None
            try:
                magasin_id = int(self.data.get('magasin')) if self.data.get('magasin') else None
            except (TypeError, ValueError):
                magasin_id = None
            if not magasin_id and self.instance and getattr(self.instance, 'magasin_id', None):
                magasin_id = self.instance.magasin_id
            if magasin_id:
                produit_ids = StockActuel.objects.filter(magasin_id=magasin_id).values_list('produit_id', flat=True)
                produits_qs = Produit.objects.filter(id__in=produit_ids).order_by('nom')
            self.fields['produit'].queryset = produits_qs
            self.fields['produit'].empty_label = '— Sélectionner un produit —'
            self.fields['produit'].widget.attrs.update({'class': 'form-select'})
            self.fields['produit'].help_text = "Sélectionnez d’abord un magasin pour charger les produits disponibles."
        self.fields['quantite'].widget.attrs.update({'min': '1', 'step': '1'})
        self.fields['prix_unitaire'].widget.attrs.update({'min': '1', 'step': '1'})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Informations du crédit',
                Row(
                    Column('numero', css_class='form-group col-md-6 mb-0'),
                    Column('date', css_class='form-group col-md-6 mb-0'),
                ),
                Row(
                    Column('client', css_class='form-group col-md-6 mb-0'),
                    Column('magasin', css_class='form-group col-md-6 mb-0'),
                ),
                'produit',
                Row(
                    Column('quantite', css_class='form-group col-md-6 mb-0'),
                    Column('prix_unitaire', css_class='form-group col-md-6 mb-0'),
                ),
                'observations',
            ),
            Submit('submit', 'Enregistrer le crédit', css_class='btn btn-warning')
        )

    def clean_numero(self):
        numero = (self.cleaned_data.get('numero') or '').strip().upper()
        if not re.match(r'^CRD\d{4,}$', numero):
            raise forms.ValidationError('Numéro invalide. Format attendu: CRD0001')
        return numero

    def clean_date(self):
        d = self.cleaned_data.get('date')
        if d and d > dt_date.today():
            raise forms.ValidationError("La date ne peut pas être dans le futur.")
        return d

    def clean(self):
        cleaned = super().clean()
        magasin = cleaned.get('magasin')
        produit = cleaned.get('produit')
        if magasin and produit:
            # Vérifie que le produit est disponible pour ce magasin
            if not StockActuel.objects.filter(magasin=magasin, produit=produit).exists():
                self.add_error('produit', "Le produit sélectionné n'est pas disponible dans le magasin choisi.")
        return cleaned


class PaiementForm(forms.ModelForm):
    """
    Formulaire pour enregistrer un paiement
    """
    class Meta:
        model = Paiement
        fields = ['date_paiement', 'montant', 'mode_paiement', 'reference', 'observations']
        widgets = {
            'date_paiement': forms.DateInput(attrs={'type': 'date'}),
            'observations': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Contraintes d'entrée pour des valeurs entières
        if 'montant' in self.fields:
            self.fields['montant'].widget.attrs.update({'min': '1', 'step': '1'})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Informations du paiement',
                Row(
                    Column('date_paiement', css_class='form-group col-md-6 mb-0'),
                    Column('montant', css_class='form-group col-md-6 mb-0'),
                ),
                Row(
                    Column('mode_paiement', css_class='form-group col-md-6 mb-0'),
                    Column('reference', css_class='form-group col-md-6 mb-0'),
                ),
                'observations',
            ),
            Submit('submit', 'Enregistrer le paiement', css_class='btn btn-success')
        )

    def clean_reference(self):
        ref = self.cleaned_data.get('reference')
        return ref.strip().upper() if ref else ref
