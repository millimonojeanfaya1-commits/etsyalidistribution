from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from ventes.models import Client, Magasin
from fournisseurs.models import Produit


class CreditClient(models.Model):
    """
    Modèle pour les crédits clients
    Correspond au Module 3 : Crédits clients
    """
    numero = models.CharField(max_length=50, unique=True, verbose_name="N° de crédit")
    date = models.DateField(verbose_name="Date de crédit")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, verbose_name="Magasin")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, verbose_name="Produit")
    quantite = models.DecimalField(max_digits=10, decimal_places=2, 
                                 verbose_name="Quantité",
                                 validators=[MinValueValidator(Decimal('0.01'))])
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, 
                                      verbose_name="Prix unitaire",
                                      validators=[MinValueValidator(Decimal('0.01'))])
    montant_total = models.DecimalField(max_digits=12, decimal_places=2, 
                                      verbose_name="Montant total", editable=False)
    montant_paye = models.DecimalField(max_digits=12, decimal_places=2, 
                                     default=0, verbose_name="Montant payé",
                                     validators=[MinValueValidator(Decimal('0'))])
    solde_restant = models.DecimalField(max_digits=12, decimal_places=2, 
                                      verbose_name="Solde restant", editable=False)
    observations = models.TextField(blank=True, null=True, verbose_name="Observations")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Crédit Client"
        verbose_name_plural = "Crédits Clients"
        ordering = ['-date', '-date_creation']
    
    def save(self, *args, **kwargs):
        """
        Calcul automatique du montant total et du solde restant
        """
        self.montant_total = self.quantite * self.prix_unitaire
        self.solde_restant = self.montant_total - self.montant_paye
        super().save(*args, **kwargs)
    
    @property
    def est_solde(self):
        """Vérifie si le crédit est entièrement payé"""
        return self.solde_restant <= 0
    
    @property
    def taux_recouvrement(self):
        """Calcule le taux de recouvrement en pourcentage"""
        if self.montant_total > 0:
            return (self.montant_paye / self.montant_total) * 100
        return 0
    
    def __str__(self):
        return f"{self.numero} - {self.client} - {self.date}"


class Paiement(models.Model):
    """
    Modèle pour les paiements des crédits
    """
    credit = models.ForeignKey(CreditClient, on_delete=models.CASCADE, 
                              related_name='paiements', verbose_name="Crédit")
    date_paiement = models.DateField(verbose_name="Date de paiement")
    montant = models.DecimalField(max_digits=12, decimal_places=2, 
                                verbose_name="Montant payé",
                                validators=[MinValueValidator(Decimal('0.01'))])
    mode_paiement = models.CharField(max_length=50, verbose_name="Mode de paiement",
                                   choices=[
                                       ('especes', 'Espèces'),
                                       ('cheque', 'Chèque'),
                                       ('virement', 'Virement'),
                                       ('mobile_money', 'Mobile Money'),
                                   ])
    reference = models.CharField(max_length=100, blank=True, null=True, 
                               verbose_name="Référence")
    observations = models.TextField(blank=True, null=True, verbose_name="Observations")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-date_paiement', '-date_creation']
    
    def save(self, *args, **kwargs):
        """
        Met à jour le montant payé du crédit après enregistrement du paiement
        """
        super().save(*args, **kwargs)
        # Recalculer le montant total payé pour ce crédit
        total_paye = self.credit.paiements.aggregate(
            total=models.Sum('montant')
        )['total'] or 0
        self.credit.montant_paye = total_paye
        self.credit.save()
    
    def __str__(self):
        return f"Paiement {self.montant} - {self.credit.numero}"
