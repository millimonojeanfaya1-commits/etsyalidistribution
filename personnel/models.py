from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Employe(models.Model):
    """
    Modèle pour les employés
    Correspond au Module 6 : Gestion du personnel et salaires
    """
    numero = models.CharField(max_length=50, unique=True, verbose_name="N° employé")
    nom = models.CharField(max_length=200, verbose_name="Nom")
    prenoms = models.CharField(max_length=200, verbose_name="Prénoms")
    matricule = models.CharField(max_length=50, unique=True, verbose_name="Matricule")
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    fonction = models.CharField(max_length=200, verbose_name="Fonction")
    salaire_base = models.DecimalField(max_digits=12, decimal_places=2, 
                                     verbose_name="Salaire de base",
                                     validators=[MinValueValidator(Decimal('0'))])
    prime_performance = models.DecimalField(max_digits=12, decimal_places=2, 
                                          default=0, verbose_name="Prime de performance",
                                          validators=[MinValueValidator(Decimal('0'))])
    
    # Informations personnelles
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    adresse = models.TextField(blank=True, null=True, verbose_name="Adresse")
    date_naissance = models.DateField(blank=True, null=True, verbose_name="Date de naissance")
    
    # Statut
    actif = models.BooleanField(default=True, verbose_name="Actif")
    date_sortie = models.DateField(blank=True, null=True, verbose_name="Date de sortie")
    motif_sortie = models.TextField(blank=True, null=True, verbose_name="Motif de sortie")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Employé"
        verbose_name_plural = "Employés"
        ordering = ['nom', 'prenoms']
    
    @property
    def nom_complet(self):
        return f"{self.nom} {self.prenoms}"
    
    @property
    def salaire_brut_mensuel(self):
        return self.salaire_base + self.prime_performance
    
    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenoms}"


class PaieSalaire(models.Model):
    """
    Modèle pour la paie des salaires
    """
    MOIS_CHOICES = [
        (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
        (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
        (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, verbose_name="Employé")
    annee = models.IntegerField(verbose_name="Année")
    mois = models.IntegerField(choices=MOIS_CHOICES, verbose_name="Mois")
    
    # Éléments de paie
    salaire_base = models.DecimalField(max_digits=12, decimal_places=2, 
                                     verbose_name="Salaire de base")
    prime_performance = models.DecimalField(max_digits=12, decimal_places=2, 
                                          default=0, verbose_name="Prime de performance")
    heures_supplementaires = models.DecimalField(max_digits=6, decimal_places=2, 
                                                default=0, verbose_name="Heures supplémentaires")
    taux_heure_sup = models.DecimalField(max_digits=10, decimal_places=2, 
                                       default=0, verbose_name="Taux heure supplémentaire")
    autres_primes = models.DecimalField(max_digits=12, decimal_places=2, 
                                      default=0, verbose_name="Autres primes")
    
    # Déductions
    avances = models.DecimalField(max_digits=12, decimal_places=2, 
                                default=0, verbose_name="Avances")
    retenues = models.DecimalField(max_digits=12, decimal_places=2, 
                                 default=0, verbose_name="Autres retenues")
    
    # Calculs
    salaire_brut = models.DecimalField(max_digits=12, decimal_places=2, 
                                     verbose_name="Salaire brut", editable=False)
    salaire_net = models.DecimalField(max_digits=12, decimal_places=2, 
                                    verbose_name="Salaire net", editable=False)
    
    # Statut
    paye = models.BooleanField(default=False, verbose_name="Payé")
    date_paiement = models.DateField(blank=True, null=True, verbose_name="Date de paiement")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Paie Salaire"
        verbose_name_plural = "Paies Salaires"
        unique_together = ['employe', 'annee', 'mois']
        ordering = ['-annee', '-mois', 'employe']
    
    def save(self, *args, **kwargs):
        """
        Calcul automatique du salaire brut et net
        """
        # Calcul du salaire brut
        montant_heures_sup = self.heures_supplementaires * self.taux_heure_sup
        self.salaire_brut = (self.salaire_base + self.prime_performance + 
                           montant_heures_sup + self.autres_primes)
        
        # Calcul du salaire net
        self.salaire_net = self.salaire_brut - self.avances - self.retenues
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employe.nom} - {self.get_mois_display()} {self.annee}"


class Conge(models.Model):
    """
    Modèle pour les congés des employés
    """
    TYPE_CONGE_CHOICES = [
        ('annuel', 'Congé annuel'),
        ('maladie', 'Congé maladie'),
        ('maternite', 'Congé maternité'),
        ('sans_solde', 'Congé sans solde'),
        ('exceptionnel', 'Congé exceptionnel'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, verbose_name="Employé")
    type_conge = models.CharField(max_length=20, choices=TYPE_CONGE_CHOICES, 
                                verbose_name="Type de congé")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    nb_jours = models.IntegerField(verbose_name="Nombre de jours", editable=False)
    motif = models.TextField(blank=True, null=True, verbose_name="Motif")
    approuve = models.BooleanField(default=False, verbose_name="Approuvé")
    date_approbation = models.DateField(blank=True, null=True, verbose_name="Date d'approbation")
    
    # Champs automatiques
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Congé"
        verbose_name_plural = "Congés"
        ordering = ['-date_debut']
    
    def save(self, *args, **kwargs):
        """
        Calcul automatique du nombre de jours
        """
        if self.date_debut and self.date_fin:
            self.nb_jours = (self.date_fin - self.date_debut).days + 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employe.nom} - {self.get_type_conge_display()} ({self.date_debut})"
