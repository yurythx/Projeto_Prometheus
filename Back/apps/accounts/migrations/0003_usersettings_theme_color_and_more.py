# Generated by Django 4.2.10 on 2025-05-09 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_usersettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='theme_color',
            field=models.CharField(choices=[('blue', 'Azul'), ('purple', 'Roxo'), ('green', 'Verde'), ('red', 'Vermelho'), ('orange', 'Laranja')], default='blue', max_length=10),
        ),
        migrations.AddField(
            model_name='usersettings',
            name='use_system_theme',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='theme',
            field=models.CharField(choices=[('light', 'Claro'), ('dark', 'Escuro'), ('sepia', 'Sépia')], default='dark', max_length=10),
        ),
    ]
