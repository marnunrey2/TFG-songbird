# Generated by Django 5.0.2 on 2024-02-12 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('populate', '0005_alter_song_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
