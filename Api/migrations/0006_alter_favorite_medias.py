
# Generated by Django 4.1 on 2022-11-20 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0005_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='medias',
            field=models.ManyToManyField(blank=True, to='Api.media'),
        ),
    ]