# Generated by Django 3.1.4 on 2020-12-08 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20201208_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='player2',
            field=models.CharField(max_length=50, null=True),
        ),
    ]