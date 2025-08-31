from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column
from .models import Fournisseur, Produit, Livraison


class FournisseurForm(forms.ModelForm):
    """
    Formulaire pour créer/modifier un fournisseur
    """
    class Meta:
        model = Fournisseur
        fields = ['nom', 'adresse', 'telephone', 'email']
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Informations du fournisseur',
                'nom',
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


class ProduitForm(forms.ModelForm):
    """
    Formulaire pour créer/modifier un produit
    """
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'unite_mesure', 'prix_vente_conseille']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Informations du produit',
                'nom',
                'description',
                Row(
                    Column('unite_mesure', css_class='form-group col-md-6 mb-0'),
                    Column('prix_vente_conseille', css_class='form-group col-md-6 mb-0'),
                ),
            ),
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )


class LivraisonForm(forms.ModelForm):
    """
    Formulaire pour enregistrer une livraison
    """
    class Meta:
        model = Livraison
        fields = ['numero_enregistrement', 'date', 'fournisseur', 'produit', 
                 'quantite_livree', 'prix_achat_unitaire', 'observations']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'observations': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Informations de la livraison',
                Row(
                    Column('numero_enregistrement', css_class='form-group col-md-6 mb-0'),
                    Column('date', css_class='form-group col-md-6 mb-0'),
                ),
                Row(
                    Column('fournisseur', css_class='form-group col-md-6 mb-0'),
                    Column('produit', css_class='form-group col-md-6 mb-0'),
                ),
                Row(
                    Column('quantite_livree', css_class='form-group col-md-6 mb-0'),
                    Column('prix_achat_unitaire', css_class='form-group col-md-6 mb-0'),
                ),
                'observations',
            ),
            Submit('submit', 'Enregistrer la livraison', css_class='btn btn-success')
        )

    def clean_numero_enregistrement(self):
        num = self.cleaned_data.get('numero_enregistrement')
        return num.strip().upper() if num else num
