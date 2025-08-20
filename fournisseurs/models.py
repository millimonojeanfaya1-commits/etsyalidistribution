from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Fournisseur(models.Model):
    """
    Modèle pour les fournisseurs
    """
    nom = models.CharField(max_length=200, verbose_name="Nom du fournisseur")
    adresse = models.TextField(blank=True, null=True, verbose_name="Adresse")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")
    
    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Produit(models.Model):
    """
    Modèle pour les produits
    """
    nom = models.CharField(max_length=200, verbose_name="Nom du produit")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    unite_mesure = models.CharField(max_length=50, verbose_name="Unité de mesure", 
                                   help_text="Ex: kg, litre, pièce, etc.")
    prix_vente_conseille = models.DecimalField(max_digits=10, decimal_places=2, 
                                             verbose_name="Prix de vente conseillé",
                                             validators=[MinValueValidator(Decimal('0.01'))])
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Livraison(models.Model):
    """
    Modèle pour les livraisons des fournisseurs
    Correspond au Module 1 : Gestion des fournisseurs
    """
    numero_enregistrement = models.CharField(max_length=50, unique=True, 
                                           verbose_name="N° d'enregistrement")
    date = models.DateField(verbose_name="Date de livraison")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, 
                                   verbose_name="Fournisseur")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, 
                               verbose_name="Produit livré")
    quantite_livree = models.DecimalField(max_digits=10, decimal_places=2, 
                                        verbose_name="Quantité livrée",
                                        validators=[MinValueValidator(Decimal('0.01'))])
    prix_achat_unitaire = models.DecimalField(max_digits=10, decimal_places=2, 
                                            verbose_name="Prix d'achat unitaire",
                                            validators=[MinValueValidator(Decimal('0.01'))])
    montant_total_achat = models.DecimalField(max_digits=12, decimal_places=2, 
                                            verbose_name="Montant total d'achat",
                                            editable=False)
    observations = models.TextField(blank=True, null=True, verbose_name="Observations")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Livraison"
        verbose_name_plural = "Livraisons"
        ordering = ['-date', '-date_creation']
    
    def save(self, *args, **kwargs):
        """
        Calcul automatique du montant total d'achat
        """
        self.montant_total_achat = self.quantite_livree * self.prix_achat_unitaire
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero_enregistrement} - {self.fournisseur.nom} - {self.date}"
