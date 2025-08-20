from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from fournisseurs.models import Produit


class Magasin(models.Model):
    """
    Modèle pour les magasins/points de vente
    """
    nom = models.CharField(max_length=200, verbose_name="Nom du magasin")
    adresse = models.TextField(blank=True, null=True, verbose_name="Adresse")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    responsable = models.CharField(max_length=200, blank=True, null=True, verbose_name="Responsable")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Magasin"
        verbose_name_plural = "Magasins"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Client(models.Model):
    """
    Modèle pour les clients
    """
    nom = models.CharField(max_length=200, verbose_name="Nom du client")
    prenom = models.CharField(max_length=200, blank=True, null=True, verbose_name="Prénom")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    adresse = models.TextField(blank=True, null=True, verbose_name="Adresse")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['nom', 'prenom']
    
    def __str__(self):
        if self.prenom:
            return f"{self.nom} {self.prenom}"
        return self.nom


class Vente(models.Model):
    """
    Modèle pour les ventes
    Correspond au Module 2 : Gestion des ventes
    """
    TYPE_VENTE_CHOICES = [
        ('cash', 'Cash'),
        ('credit', 'Crédit'),
    ]
    
    numero = models.CharField(max_length=50, unique=True, verbose_name="N° de vente")
    date = models.DateField(verbose_name="Date de vente")
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, verbose_name="Magasin")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, verbose_name="Produit")
    quantite_vendue = models.DecimalField(max_digits=10, decimal_places=2, 
                                        verbose_name="Quantité vendue",
                                        validators=[MinValueValidator(Decimal('0.01'))])
    type_vente = models.CharField(max_length=10, choices=TYPE_VENTE_CHOICES, 
                                 verbose_name="Type de vente")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, 
                                      verbose_name="Prix unitaire",
                                      validators=[MinValueValidator(Decimal('0.01'))])
    total_vente = models.DecimalField(max_digits=12, decimal_places=2, 
                                    verbose_name="Total vente", editable=False)
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
        ordering = ['-date', '-date_creation']
    
    def save(self, *args, **kwargs):
        """
        Calcul automatique du total de vente
        """
        self.total_vente = self.quantite_vendue * self.prix_unitaire
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero} - {self.client} - {self.date}"


class Commercial(models.Model):
    """
    Modèle pour les commerciaux/vendeurs
    """
    nom = models.CharField(max_length=200, verbose_name="Nom")
    prenom = models.CharField(max_length=200, verbose_name="Prénom")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, 
                               verbose_name="Magasin principal")
    commission_pourcentage = models.DecimalField(max_digits=5, decimal_places=2, 
                                                default=0, verbose_name="Commission (%)")
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Commercial"
        verbose_name_plural = "Commerciaux"
        ordering = ['nom', 'prenom']
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
