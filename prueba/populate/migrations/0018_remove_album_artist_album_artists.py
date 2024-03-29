# Generated by Django 5.0.2 on 2024-03-28 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('populate', '0017_remove_song_artist_song_artists'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='artist',
        ),
        migrations.AddField(
            model_name='album',
            name='artists',
            field=models.ManyToManyField(to='populate.artist'),
        ),
    ]
