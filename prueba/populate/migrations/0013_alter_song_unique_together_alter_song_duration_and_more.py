# Generated by Django 5.0.2 on 2024-03-27 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('populate', '0012_alter_album_image_alter_album_release_date'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='song',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='song',
            name='duration',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='image',
            field=models.CharField(blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='position',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='release_date',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('songs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlists', to='populate.song')),
            ],
        ),
        migrations.RemoveField(
            model_name='song',
            name='album',
        ),
        migrations.RemoveField(
            model_name='song',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='song',
            name='collaborators',
        ),
        migrations.RemoveField(
            model_name='song',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='song',
            name='lyrics',
        ),
        migrations.RemoveField(
            model_name='song',
            name='reproductions',
        ),
        migrations.RemoveField(
            model_name='song',
            name='video',
        ),
    ]
