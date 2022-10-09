# Generated by Django 4.1.2 on 2022-10-08 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_meunegocio_transacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='meunegocio',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='negocios', related_query_name='negocio', to=settings.AUTH_USER_MODEL, verbose_name='Meu Negocio'),
            preserve_default=False,
        ),
    ]
