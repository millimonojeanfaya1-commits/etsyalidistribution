from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column
from .models import Magasin, Client, Vente, Commercial


class MagasinForm(forms.ModelForm):
    """
    Formulaire pour créer/modifier un magasin
    """
    class Meta:
        model = Magasin
        fields = ['nom', 'adresse', 'telephone', 'responsable']
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Informations du magasin',
                'nom',
                Row(
                    Column('responsable', css_class='form-group col-md-6 mb-0'),
                    Column('telephone', css_class='form-group col-md-6 mb-0'),
                ),
                'adresse',
            ),
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        return nom.upper().strip() if nom else nom

    def clean_responsable(self):
        resp = self.cleaned_data.get('responsable')
        return resp.upper().strip() if resp else resp


class ClientForm(forms.ModelForm):
    """
    Formulaire pour créer/modifier un client
    """
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'telephone', 'email', 'adresse']
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Informations du client',
                Row(
                    Column('nom', css_class='form-group col-md-6 mb-0'),
                    Column('prenom', css_class='form-group col-md-6 mb-0'),
                ),
                Row(
                    Column('telephone', css_class='form-group col-md-6 mb-0'),
                    Column('email', css_class='form-group col-md-6 mb-0'),
                ),
                'adresse',
            ),
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        return nom.upper().strip() if nom else nom

    def clean_prenom(self):
        prenom = self.cleaned_data.get('prenom')
        return prenom.upper().strip() if prenom else prenom


class VenteForm(forms.ModelForm):
    """
    Formulaire pour enregistrer une vente
    """
    class Meta:
        model = Vente
        fields = ['numero', 'date', 'magasin', 'client', 'produit', 
                 'quantite_vendue', 'prix_unitaire', 'type_vente']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Informations de la vente',
                Row(
                    Column('numero', css_class='form-group col-md-6 mb-0'),
                    Column('date', css_class='form-group col-md-6 mb-0'),
                ),
                Row(
                    Column('magasin', css_class='form-group col-md-6 mb-0'),
                    Column('client', css_class='form-group col-md-6 mb-0'),
                ),
                'produit',
                Row(
                    Column('quantite_vendue', css_class='form-group col-md-4 mb-0'),
                    Column('prix_unitaire', css_class='form-group col-md-4 mb-0'),
                    Column('type_vente', css_class='form-group col-md-4 mb-0'),
                ),
            ),
            Submit('submit', 'Enregistrer la vente', css_class='btn btn-success')
        )

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        return numero.upper().strip() if numero else numero
