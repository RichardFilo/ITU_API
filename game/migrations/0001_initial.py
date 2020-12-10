# Generated by Django 3.1.4 on 2020-12-08 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chessboard', models.CharField(default='00100010001000101000100010001000001000100010001000000000000000000000000000000000100010001000100000100010001000101000100010001000', max_length=128)),
                ('onTurn', models.BooleanField(default=True)),
                ('player1', models.CharField(max_length=50)),
                ('player2', models.CharField(max_length=50)),
                ('state', models.CharField(default='lobby', max_length=50)),
            ],
        ),
    ]