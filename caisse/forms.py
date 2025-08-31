from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit
from .models import MouvementCaisse


class MouvementCaisseForm(forms.ModelForm):
    class Meta:
        model = MouvementCaisse
        fields = ['date', 'libelle', 'montant_entree', 'montant_sortie', 'observations']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'observations': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Mouvement de caisse',
                Row(
                    Column('date', css_class='form-group col-md-6 mb-0'),
                    Column('libelle', css_class='form-group col-md-6 mb-0'),
                ),
                Row(
                    Column('montant_entree', css_class='form-group col-md-6 mb-0'),
                    Column('montant_sortie', css_class='form-group col-md-6 mb-0'),
                ),
                'observations',
            ),
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )

    def clean_observations(self):
        obs = self.cleaned_data.get('observations')
        return obs.strip() if obs else obs
