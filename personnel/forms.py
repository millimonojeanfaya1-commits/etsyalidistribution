from django import forms
from django.core.validators import RegexValidator
from .models import Employe, PaieSalaire


class EmployeForm(forms.ModelForm):
    # Rendre le champ 'numero' optionnel au niveau du formulaire
    numero = forms.CharField(required=False, label="N° employé")
    telephone = forms.CharField(
        required=False,
        validators=[RegexValidator(r"^[0-9 +().-]{6,20}$", "Numéro invalide")],
        widget=forms.TextInput(attrs={'placeholder': '+224 6x xx xx xx'}),
        label="Téléphone",
    )

    class Meta:
        model = Employe
        # Inclure les champs pertinents (exclure les auto fields)
        fields = [
            'numero', 'nom', 'prenoms', 'matricule', 'date_embauche', 'fonction',
            'salaire_base', 'prime_performance',
            'telephone', 'email', 'adresse', 'date_naissance',
            'actif', 'date_sortie', 'motif_sortie',
        ]
        widgets = {
            'date_embauche': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_sortie': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'numero': "N° employé",
            'prenoms': "Prénoms",
            'fonction': "Fonction",
            'salaire_base': "Salaire de base",
            'prime_performance': "Prime de performance",
            'date_embauche': "Date d'embauche",
            'date_naissance': "Date de naissance",
            'date_sortie': "Date de sortie",
            'motif_sortie': "Motif de sortie",
        }
        help_texts = {
            'prime_performance': "0 si aucune prime",
            'numero': "Laissez vide pour générer automatiquement (ex: EMP-0001)",
        }
        error_messages = {
            'numero': {
                'unique': "Ce numéro d'employé existe déjà.",
                'required': "Le numéro d'employé est requis.",
            },
            'matricule': {
                'unique': "Ce matricule existe déjà.",
                'required': "Le matricule est requis.",
            },
            'email': {
                'invalid': "Adresse e-mail invalide.",
            },
        }

    def clean_nom(self):
        return self.cleaned_data['nom'].strip().upper()

    def clean_prenoms(self):
        # Uppercase full field
        return self.cleaned_data['prenoms'].strip().upper()

    def clean_matricule(self):
        return self.cleaned_data['matricule'].strip().upper()

    def clean_fonction(self):
        return self.cleaned_data['fonction'].strip().upper()

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if not numero:
            return ''  # sera généré au save()
        return numero.strip().upper()

    @staticmethod
    def _generate_numero():
        prefix = 'EMP-'
        numeros = (
            Employe.objects
            .filter(numero__startswith=prefix)
            .values_list('numero', flat=True)
        )
        max_seq = 0
        for n in numeros:
            try:
                seq = int(str(n).split('-')[-1])
                if seq > max_seq:
                    max_seq = seq
            except Exception:
                continue
        return f"{prefix}{max_seq + 1:04d}"

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Si le numéro est vide, le générer automatiquement
        if not instance.numero:
            instance.numero = self._generate_numero()
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class PaieSalaireForm(forms.ModelForm):
    """Formulaire de création/édition d'une paie"""

    class Meta:
        model = PaieSalaire
        fields = [
            'employe', 'annee', 'mois',
            'salaire_base', 'prime_performance',
            'heures_supplementaires', 'taux_heure_sup', 'autres_primes',
            'avances', 'retenues',
            'paye', 'date_paiement',
        ]
        widgets = {
            'annee': forms.NumberInput(attrs={'min': 2000, 'max': 2100, 'class': 'form-control'}),
            'mois': forms.Select(attrs={'class': 'form-select'}),
            'salaire_base': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'class': 'form-control'}),
            'prime_performance': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'class': 'form-control'}),
            'heures_supplementaires': forms.NumberInput(attrs={'min': 0, 'step': '0.25', 'class': 'form-control'}),
            'taux_heure_sup': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'class': 'form-control'}),
            'autres_primes': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'class': 'form-control'}),
            'avances': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'class': 'form-control'}),
            'retenues': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'class': 'form-control'}),
            'date_paiement': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'heures_supplementaires': 'Heures sup.',
            'taux_heure_sup': 'Taux heure sup.',
            'autres_primes': 'Autres primes',
        }

    def clean_annee(self):
        annee = self.cleaned_data.get('annee')
        if annee and (annee < 2000 or annee > 2100):
            raise forms.ValidationError("Année invalide (2000-2100).")
        return annee

