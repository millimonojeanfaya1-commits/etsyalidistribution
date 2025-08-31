from django import forms
from .models import Charge, CategorieCharge


class ChargeForm(forms.ModelForm):
    """Formulaire de création/édition d'une Charge"""

    numero = forms.CharField(required=False, label="N° de charge")

    class Meta:
        model = Charge
        fields = [
            'numero', 'date', 'categorie', 'libelle', 'montant',
            'fournisseur', 'facture_numero', 'mode_paiement',
            'observations', 'payee', 'date_paiement',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'class': 'form-control'}),
            'fournisseur': forms.TextInput(attrs={'class': 'form-control'}),
            'facture_numero': forms.TextInput(attrs={'class': 'form-control'}),
            'mode_paiement': forms.Select(attrs={'class': 'form-select'}),
            'observations': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'date_paiement': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        payee = cleaned.get('payee')
        date_paiement = cleaned.get('date_paiement')
        if payee and not date_paiement:
            self.add_error('date_paiement', "La date de paiement est requise lorsque la charge est marquée comme payée.")
        return cleaned

    def clean_libelle(self):
        lib = self.cleaned_data.get('libelle')
        return lib.upper() if lib else lib

    def clean_numero(self):
        num = self.cleaned_data.get('numero')
        return num.strip().upper() if num else num

    def clean_facture_numero(self):
        num = self.cleaned_data.get('facture_numero')
        return num.strip().upper() if num else num

    def clean_fournisseur(self):
        four = self.cleaned_data.get('fournisseur')
        return four.strip().upper() if four else four

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Générer un numéro si non fourni: CHG0001
        if not instance.numero:
            instance.numero = self._generate_numero()
        if commit:
            instance.save()
        return instance

    def _generate_numero(self):
        prefix = 'CHG'
        # Compte simple pour incrémenter (peut être amélioré par année)
        last = Charge.objects.filter(numero__startswith=prefix).order_by('-id').first()
        if last and last.numero.startswith(prefix):
            try:
                n = int(''.join(filter(str.isdigit, last.numero))) + 1
            except ValueError:
                n = 1
        else:
            n = 1
        return f"{prefix}{n:04d}"
