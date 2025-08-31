# Generated manually to add libelle field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caisse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mouvementcaisse',
            name='libelle',
            field=models.CharField(default='', max_length=200, verbose_name='Libellé'),
            preserve_default=False,
        ),
    ]
