# Generated by Django 4.1.7 on 2023-02-16 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=200)),
                ('pic', models.FileField(default='default.img', upload_to='Buyer_profile')),
            ],
        ),
    ]
