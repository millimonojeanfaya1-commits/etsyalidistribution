from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class CategorieCharge(models.Model):
    """
    Modèle pour les catégories de charges
    """
    nom = models.CharField(max_length=200, unique=True, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    type_charge = models.CharField(max_length=20, choices=[
        ('fixe', 'Charge fixe'),
        ('variable', 'Charge variable'),
    ], verbose_name="Type de charge")
    
    class Meta:
        verbose_name = "Catégorie de Charge"
        verbose_name_plural = "Catégories de Charges"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.get_type_charge_display()})"


class Charge(models.Model):
    """
    Modèle pour les charges
    Correspond au Module 7 : Gestion des charges
    """
    numero = models.CharField(max_length=50, unique=True, verbose_name="N° de charge")
    date = models.DateField(verbose_name="Date de la charge")
    categorie = models.ForeignKey(CategorieCharge, on_delete=models.CASCADE, 
                                verbose_name="Catégorie")
    libelle = models.CharField(max_length=300, verbose_name="Libellé")
    montant = models.DecimalField(max_digits=12, decimal_places=2, 
                                verbose_name="Montant",
                                validators=[MinValueValidator(Decimal('0.01'))])
    fournisseur = models.CharField(max_length=200, blank=True, null=True, 
                                 verbose_name="Fournisseur/Prestataire")
    facture_numero = models.CharField(max_length=100, blank=True, null=True, 
                                    verbose_name="N° de facture")
    mode_paiement = models.CharField(max_length=50, verbose_name="Mode de paiement",
                                   choices=[
                                       ('especes', 'Espèces'),
                                       ('cheque', 'Chèque'),
                                       ('virement', 'Virement'),
                                       ('carte', 'Carte bancaire'),
                                       ('mobile_money', 'Mobile Money'),
                                   ])
    observations = models.TextField(blank=True, null=True, verbose_name="Observations")
    
    # Statut
    payee = models.BooleanField(default=True, verbose_name="Payée")
    date_paiement = models.DateField(blank=True, null=True, verbose_name="Date de paiement")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Charge"
        verbose_name_plural = "Charges"
        ordering = ['-date', '-date_creation']
    
    @property
    def type_charge(self):
        return self.categorie.type_charge
    
    def __str__(self):
        return f"{self.numero} - {self.libelle} - {self.montant}"


class BudgetAnnuel(models.Model):
    """
    Modèle pour le budget annuel par catégorie
    """
    annee = models.IntegerField(verbose_name="Année")
    categorie = models.ForeignKey(CategorieCharge, on_delete=models.CASCADE, 
                                verbose_name="Catégorie")
    budget_prevu = models.DecimalField(max_digits=12, decimal_places=2, 
                                     verbose_name="Budget prévu",
                                     validators=[MinValueValidator(Decimal('0'))])
    budget_realise = models.DecimalField(max_digits=12, decimal_places=2, 
                                       default=0, verbose_name="Budget réalisé", 
                                       editable=False)
    ecart = models.DecimalField(max_digits=12, decimal_places=2, 
                              verbose_name="Écart", editable=False)
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Budget Annuel"
        verbose_name_plural = "Budgets Annuels"
        unique_together = ['annee', 'categorie']
        ordering = ['-annee', 'categorie']
    
    def save(self, *args, **kwargs):
        """
        Calcul automatique de l'écart
        """
        self.ecart = self.budget_realise - self.budget_prevu
        super().save(*args, **kwargs)
    
    @property
    def taux_realisation(self):
        """Calcule le taux de réalisation en pourcentage"""
        if self.budget_prevu > 0:
            return (self.budget_realise / self.budget_prevu) * 100
        return 0
    
    def __str__(self):
        return f"Budget {self.annee} - {self.categorie.nom}"


class PlanificationCharge(models.Model):
    """
    Modèle pour la planification des charges récurrentes
    """
    FREQUENCE_CHOICES = [
        ('mensuelle', 'Mensuelle'),
        ('trimestrielle', 'Trimestrielle'),
        ('semestrielle', 'Semestrielle'),
        ('annuelle', 'Annuelle'),
    ]
    
    categorie = models.ForeignKey(CategorieCharge, on_delete=models.CASCADE, 
                                verbose_name="Catégorie")
    libelle = models.CharField(max_length=300, verbose_name="Libellé")
    montant_prevu = models.DecimalField(max_digits=12, decimal_places=2, 
                                      verbose_name="Montant prévu",
                                      validators=[MinValueValidator(Decimal('0.01'))])
    frequence = models.CharField(max_length=20, choices=FREQUENCE_CHOICES, 
                               verbose_name="Fréquence")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(blank=True, null=True, verbose_name="Date de fin")
    active = models.BooleanField(default=True, verbose_name="Active")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Planification Charge"
        verbose_name_plural = "Planifications Charges"
        ordering = ['categorie', 'libelle']
    
    def __str__(self):
        return f"{self.libelle} - {self.get_frequence_display()}"
