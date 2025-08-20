from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column
from .models import CreditClient, Paiement
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
        self.fields['quantite'].widget.attrs.update({'min': '0.01', 'step': '0.01'})
        self.fields['prix_unitaire'].widget.attrs.update({'min': '0.01', 'step': '0.01'})
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
        numero = (self.cleaned_data.get('numero') or '').strip()
        if not re.match(r'^CRD\d{4,}$', numero):
            raise forms.ValidationError('Numéro invalide. Format attendu: CRD0001')
        return numero

    def clean_date(self):
        d = self.cleaned_data.get('date')
        if d and d > dt_date.today():
            raise forms.ValidationError("La date ne peut pas être dans le futur.")
        return d


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
