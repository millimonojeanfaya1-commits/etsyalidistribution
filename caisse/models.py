from django.db import models


class MouvementCaisse(models.Model):
    date = models.DateField()
    libelle = models.CharField(max_length=200, verbose_name="Libellé")
    montant_entree = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    montant_sortie = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observations = models.TextField(blank=True)

    class Meta:
        ordering = ['-date', '-id']
        verbose_name = 'Mouvement de caisse'
        verbose_name_plural = 'Mouvements de caisse'

    def __str__(self):
        net = (self.montant_entree or 0) - (self.montant_sortie or 0)
        return f"{self.date} - {self.libelle} | +{self.montant_entree} / -{self.montant_sortie} (net: {net})"
