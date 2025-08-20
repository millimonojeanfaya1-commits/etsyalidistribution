from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from ventes.models import Magasin, Commercial
from fournisseurs.models import Produit


class AnalyseProfit(models.Model):
    """
    Modèle pour l'analyse des profits
    Correspond au Module 8 : Profits
    """
    numero = models.CharField(max_length=50, unique=True, verbose_name="N° d'analyse")
    date = models.DateField(verbose_name="Date d'analyse")
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, verbose_name="Magasin")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, verbose_name="Produit")
    commercial = models.ForeignKey(Commercial, on_delete=models.CASCADE, 
                                 verbose_name="Commercial", blank=True, null=True)
    
    # Données d'achat
    quantite_achetee = models.DecimalField(max_digits=10, decimal_places=2, 
                                         verbose_name="Quantité achetée",
                                         validators=[MinValueValidator(Decimal('0'))])
    prix_achat_unitaire = models.DecimalField(max_digits=10, decimal_places=2, 
                                            verbose_name="Prix d'achat unitaire",
                                            validators=[MinValueValidator(Decimal('0.01'))])
    montant_achat = models.DecimalField(max_digits=12, decimal_places=2, 
                                      verbose_name="Montant d'achat", editable=False)
    
    # Données de vente
    quantite_vendue = models.DecimalField(max_digits=10, decimal_places=2, 
                                        verbose_name="Quantité vendue",
                                        validators=[MinValueValidator(Decimal('0'))])
    prix_vente_unitaire = models.DecimalField(max_digits=10, decimal_places=2, 
                                            verbose_name="Prix de vente unitaire",
                                            validators=[MinValueValidator(Decimal('0.01'))])
    montant_vente = models.DecimalField(max_digits=12, decimal_places=2, 
                                      verbose_name="Montant de vente", editable=False)
    
    # Calculs de profit
    profit_brut = models.DecimalField(max_digits=12, decimal_places=2, 
                                    verbose_name="Profit brut", editable=False)
    charges_associees = models.DecimalField(max_digits=12, decimal_places=2, 
                                          default=0, verbose_name="Charges associées",
                                          validators=[MinValueValidator(Decimal('0'))])
    profit_net = models.DecimalField(max_digits=12, decimal_places=2, 
                                   verbose_name="Profit net", editable=False)
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Analyse de Profit"
        verbose_name_plural = "Analyses de Profits"
        ordering = ['-date', '-date_creation']
    
    def save(self, *args, **kwargs):
        """
        Calcul automatique des montants et profits
        """
        self.montant_achat = self.quantite_achetee * self.prix_achat_unitaire
        self.montant_vente = self.quantite_vendue * self.prix_vente_unitaire
        self.profit_brut = self.montant_vente - self.montant_achat
        self.profit_net = self.profit_brut - self.charges_associees
        super().save(*args, **kwargs)
    
    @property
    def marge_brute_pourcentage(self):
        """Calcule la marge brute en pourcentage"""
        if self.montant_vente > 0:
            return (self.profit_brut / self.montant_vente) * 100
        return 0
    
    @property
    def marge_nette_pourcentage(self):
        """Calcule la marge nette en pourcentage"""
        if self.montant_vente > 0:
            return (self.profit_net / self.montant_vente) * 100
        return 0
    
    @property
    def rentabilite_pourcentage(self):
        """Calcule la rentabilité par rapport au coût d'achat"""
        if self.montant_achat > 0:
            return (self.profit_net / self.montant_achat) * 100
        return 0
    
    def __str__(self):
        return f"{self.numero} - {self.produit.nom} - {self.magasin.nom}"


class RapportProfitMensuel(models.Model):
    """
    Modèle pour les rapports de profit mensuels
    """
    annee = models.IntegerField(verbose_name="Année")
    mois = models.IntegerField(verbose_name="Mois", choices=[
        (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
        (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
        (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
    ])
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, 
                               verbose_name="Magasin", blank=True, null=True)
    
    # Totaux mensuels
    total_achats = models.DecimalField(max_digits=15, decimal_places=2, 
                                     default=0, verbose_name="Total achats")
    total_ventes = models.DecimalField(max_digits=15, decimal_places=2, 
                                     default=0, verbose_name="Total ventes")
    total_charges = models.DecimalField(max_digits=15, decimal_places=2, 
                                      default=0, verbose_name="Total charges")
    profit_brut = models.DecimalField(max_digits=15, decimal_places=2, 
                                    default=0, verbose_name="Profit brut")
    profit_net = models.DecimalField(max_digits=15, decimal_places=2, 
                                   default=0, verbose_name="Profit net")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Rapport Profit Mensuel"
        verbose_name_plural = "Rapports Profits Mensuels"
        unique_together = ['annee', 'mois', 'magasin']
        ordering = ['-annee', '-mois', 'magasin']
    
    @property
    def marge_brute_pourcentage(self):
        """Calcule la marge brute mensuelle en pourcentage"""
        if self.total_ventes > 0:
            return (self.profit_brut / self.total_ventes) * 100
        return 0
    
    @property
    def marge_nette_pourcentage(self):
        """Calcule la marge nette mensuelle en pourcentage"""
        if self.total_ventes > 0:
            return (self.profit_net / self.total_ventes) * 100
        return 0
    
    def __str__(self):
        magasin_nom = self.magasin.nom if self.magasin else "Tous magasins"
        return f"Rapport {self.get_mois_display()} {self.annee} - {magasin_nom}"


class ClassementProduit(models.Model):
    """
    Modèle pour le classement des produits par rentabilité
    """
    periode_debut = models.DateField(verbose_name="Début de période")
    periode_fin = models.DateField(verbose_name="Fin de période")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, verbose_name="Produit")
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, 
                               verbose_name="Magasin", blank=True, null=True)
    
    # Statistiques du produit
    quantite_totale_vendue = models.DecimalField(max_digits=12, decimal_places=2, 
                                               verbose_name="Quantité totale vendue")
    chiffre_affaires = models.DecimalField(max_digits=15, decimal_places=2, 
                                         verbose_name="Chiffre d'affaires")
    cout_total_achat = models.DecimalField(max_digits=15, decimal_places=2, 
                                         verbose_name="Coût total d'achat")
    profit_total = models.DecimalField(max_digits=15, decimal_places=2, 
                                     verbose_name="Profit total")
    marge_moyenne = models.DecimalField(max_digits=5, decimal_places=2, 
                                      verbose_name="Marge moyenne (%)")
    rang_rentabilite = models.IntegerField(verbose_name="Rang rentabilité")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Classement Produit"
        verbose_name_plural = "Classements Produits"
        ordering = ['rang_rentabilite', '-profit_total']
    
    def __str__(self):
        return f"#{self.rang_rentabilite} - {self.produit.nom} (Profit: {self.profit_total})"
