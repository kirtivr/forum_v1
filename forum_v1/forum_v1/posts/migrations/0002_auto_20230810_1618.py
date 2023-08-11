# Generated by Django 3.2.18 on 2023-08-10 10:48

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='topic',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('maintenance', 'Maintenance'), ('tankers', 'Tankers'), ('suez_max', 'Suez Max'), ('engine_room', 'Engine Room')], max_length=200), blank=True, size=None),
        ),
    ]