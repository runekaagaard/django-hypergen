# Generated by Django 3.2.9 on 2021-11-23 12:31

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('hypergen', '0001_initial'),]

    operations = [
        migrations.AlterModelOptions(
        name='kv',
        options={'permissions': [('kv_hypergen_translations', 'Can edit translations')]},
        ),]