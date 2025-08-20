from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Vehicule(models.Model):
    """
    Modèle pour les véhicules du parc motorisé
    """
    matricule = models.CharField(max_length=50, unique=True, verbose_name="Matricule")
    type_vehicule = models.CharField(max_length=100, verbose_name="Type de véhicule",
                                   help_text="Ex: Camion, Voiture, Moto, etc.")
    marque = models.CharField(max_length=100, verbose_name="Marque")
    modele = models.CharField(max_length=100, verbose_name="Modèle")
    annee = models.IntegerField(verbose_name="Année")
    couleur = models.CharField(max_length=50, blank=True, null=True, verbose_name="Couleur")
    date_acquisition = models.DateField(verbose_name="Date d'acquisition")
    prix_acquisition = models.DecimalField(max_digits=12, decimal_places=2, 
                                         verbose_name="Prix d'acquisition",
                                         validators=[MinValueValidator(Decimal('0'))])
    statut = models.CharField(max_length=20, choices=[
        ('actif', 'Actif'),
        ('maintenance', 'En maintenance'),
        ('hors_service', 'Hors service'),
    ], default='actif', verbose_name="Statut")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Véhicule"
        verbose_name_plural = "Véhicules"
        ordering = ['matricule']
    
    def __str__(self):
        return f"{self.matricule} - {self.type_vehicule}"


class ConsommationCarburant(models.Model):
    """
    Modèle pour la consommation de carburant
    Correspond au Module 5 : Gestion du parc motorisé
    """
    numero = models.CharField(max_length=50, unique=True, verbose_name="N° d'enregistrement")
    date = models.DateField(verbose_name="Date")
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, 
                               verbose_name="Véhicule")
    quantite_carburant_semaine = models.DecimalField(max_digits=10, decimal_places=2, 
                                                    verbose_name="Quantité carburant/semaine (L)",
                                                    validators=[MinValueValidator(Decimal('0.01'))])
    prix_par_litre = models.DecimalField(max_digits=10, decimal_places=2, 
                                       verbose_name="Prix par litre",
                                       validators=[MinValueValidator(Decimal('0.01'))])
    montant_semaine = models.DecimalField(max_digits=12, decimal_places=2, 
                                        verbose_name="Montant par semaine", editable=False)
    montant_mois = models.DecimalField(max_digits=12, decimal_places=2, 
                                     verbose_name="Montant par mois", editable=False)
    observations = models.TextField(blank=True, null=True, verbose_name="Observations")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Consommation Carburant"
        verbose_name_plural = "Consommations Carburant"
        ordering = ['-date', '-date_creation']
    
    def save(self, *args, **kwargs):
        """
        Calcul automatique des montants
        """
        self.montant_semaine = self.quantite_carburant_semaine * self.prix_par_litre
        self.montant_mois = self.montant_semaine * 4  # Approximation 4 semaines par mois
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero} - {self.vehicule.matricule} - {self.date}"


class MaintenanceVehicule(models.Model):
    """
    Modèle pour les maintenances des véhicules
    """
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, 
                               verbose_name="Véhicule")
    date_maintenance = models.DateField(verbose_name="Date de maintenance")
    type_maintenance = models.CharField(max_length=100, verbose_name="Type de maintenance",
                                      choices=[
                                          ('vidange', 'Vidange'),
                                          ('revision', 'Révision'),
                                          ('reparation', 'Réparation'),
                                          ('controle', 'Contrôle technique'),
                                          ('autre', 'Autre'),
                                      ])
    description = models.TextField(verbose_name="Description")
    cout = models.DecimalField(max_digits=10, decimal_places=2, 
                             verbose_name="Coût",
                             validators=[MinValueValidator(Decimal('0'))])
    garage = models.CharField(max_length=200, blank=True, null=True, 
                            verbose_name="Garage/Prestataire")
    prochaine_maintenance = models.DateField(blank=True, null=True, 
                                           verbose_name="Prochaine maintenance")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Maintenance Véhicule"
        verbose_name_plural = "Maintenances Véhicules"
        ordering = ['-date_maintenance']
    
    def __str__(self):
        return f"{self.vehicule.matricule} - {self.type_maintenance} - {self.date_maintenance}"
