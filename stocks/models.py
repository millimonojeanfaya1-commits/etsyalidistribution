from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from ventes.models import Magasin, Commercial
from fournisseurs.models import Produit


class MouvementStock(models.Model):
    """
    Modèle pour les mouvements de stock
    Correspond au Module 4 : Gestion des stocks
    """
    numero = models.CharField(max_length=50, unique=True, verbose_name="N° de mouvement")
    date = models.DateField(verbose_name="Date du mouvement")
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, verbose_name="Magasin")
    commercial = models.ForeignKey(Commercial, on_delete=models.CASCADE, 
                                 verbose_name="Commercial", blank=True, null=True)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, verbose_name="Produit")
    stock_initial = models.DecimalField(max_digits=10, decimal_places=2, 
                                      verbose_name="Stock initial",
                                      validators=[MinValueValidator(Decimal('0'))])
    stock_vendu = models.DecimalField(max_digits=10, decimal_places=2, 
                                    verbose_name="Stock vendu",
                                    validators=[MinValueValidator(Decimal('0'))])
    stock_final = models.DecimalField(max_digits=10, decimal_places=2, 
                                    verbose_name="Stock final", editable=False)
    montant_ventes = models.DecimalField(max_digits=12, decimal_places=2, 
                                       verbose_name="Montant des ventes",
                                       validators=[MinValueValidator(Decimal('0'))])
    observations = models.TextField(blank=True, null=True, verbose_name="Observations")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Mouvement de Stock"
        verbose_name_plural = "Mouvements de Stock"
        ordering = ['-date', '-date_creation']
    
    def save(self, *args, **kwargs):
        """
        Calcul automatique du stock final
        """
        self.stock_final = self.stock_initial - self.stock_vendu
        super().save(*args, **kwargs)
    
    @property
    def est_rupture(self):
        """Vérifie si le stock est en rupture (< 5)"""
        return self.stock_final < 5
    
    @property
    def est_alerte(self):
        """Vérifie si le stock est en alerte (< 10)"""
        return self.stock_final < 10
    
    def __str__(self):
        return f"{self.numero} - {self.produit.nom} - {self.magasin.nom}"


class StockActuel(models.Model):
    """
    Modèle pour le stock actuel par produit et magasin
    """
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, verbose_name="Magasin")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, verbose_name="Produit")
    quantite_actuelle = models.DecimalField(max_digits=10, decimal_places=2, 
                                          verbose_name="Quantité actuelle",
                                          validators=[MinValueValidator(Decimal('0'))])
    seuil_alerte = models.DecimalField(max_digits=10, decimal_places=2, 
                                     default=10, verbose_name="Seuil d'alerte")
    prix_moyen_achat = models.DecimalField(max_digits=10, decimal_places=2, 
                                         verbose_name="Prix moyen d'achat",
                                         validators=[MinValueValidator(Decimal('0.01'))])
    valeur_stock = models.DecimalField(max_digits=12, decimal_places=2, 
                                     verbose_name="Valeur du stock", editable=False)
    
    # Champs automatiques
    date_maj = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    
    class Meta:
        verbose_name = "Stock Actuel"
        verbose_name_plural = "Stocks Actuels"
        unique_together = ['magasin', 'produit']
        ordering = ['magasin', 'produit']
    
    def save(self, *args, **kwargs):
        """
        Calcul automatique de la valeur du stock
        """
        self.valeur_stock = self.quantite_actuelle * self.prix_moyen_achat
        super().save(*args, **kwargs)
    
    @property
    def est_rupture(self):
        """Vérifie si le stock est en rupture"""
        return self.quantite_actuelle <= 0
    
    @property
    def est_alerte(self):
        """Vérifie si le stock est en alerte"""
        return self.quantite_actuelle <= self.seuil_alerte
    
    def __str__(self):
        return f"{self.produit.nom} - {self.magasin.nom} ({self.quantite_actuelle})"


class Inventaire(models.Model):
    """
    Modèle pour les inventaires
    """
    numero = models.CharField(max_length=50, unique=True, verbose_name="N° d'inventaire")
    date = models.DateField(verbose_name="Date d'inventaire")
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, verbose_name="Magasin")
    responsable = models.CharField(max_length=200, verbose_name="Responsable inventaire")
    statut = models.CharField(max_length=20, choices=[
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('valide', 'Validé'),
    ], default='en_cours', verbose_name="Statut")
    observations = models.TextField(blank=True, null=True, verbose_name="Observations")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Inventaire"
        verbose_name_plural = "Inventaires"
        ordering = ['-date']
    
    def __str__(self):
        return f"Inventaire {self.numero} - {self.magasin.nom}"


class LigneInventaire(models.Model):
    """
    Modèle pour les lignes d'inventaire
    """
    inventaire = models.ForeignKey(Inventaire, on_delete=models.CASCADE, 
                                 related_name='lignes', verbose_name="Inventaire")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, verbose_name="Produit")
    stock_theorique = models.DecimalField(max_digits=10, decimal_places=2, 
                                        verbose_name="Stock théorique")
    stock_physique = models.DecimalField(max_digits=10, decimal_places=2, 
                                       verbose_name="Stock physique")
    ecart = models.DecimalField(max_digits=10, decimal_places=2, 
                              verbose_name="Écart", editable=False)
    observations = models.TextField(blank=True, null=True, verbose_name="Observations")
    
    class Meta:
        verbose_name = "Ligne d'Inventaire"
        verbose_name_plural = "Lignes d'Inventaire"
        unique_together = ['inventaire', 'produit']
    
    def save(self, *args, **kwargs):
        """
        Calcul automatique de l'écart
        """
        self.ecart = self.stock_physique - self.stock_theorique
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.inventaire.numero} - {self.produit.nom}"
