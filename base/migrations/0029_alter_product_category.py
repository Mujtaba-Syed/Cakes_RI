# Generated by Django 4.2.5 on 2025-03-16 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_rename_decription_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Cakes', 'Cakes'), ('Cupcakes', 'Cupcakes'), ('Bouquets', 'Bouquets'), ('Customs', 'Customs')], default='Cakes', max_length=20),
        ),
    ]
