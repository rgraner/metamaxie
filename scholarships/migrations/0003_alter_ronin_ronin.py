# Generated by Django 3.2.9 on 2021-12-23 20:53

from django.db import migrations, models
import scholarships.validators


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ronin',
            name='ronin',
            field=models.CharField(max_length=46, unique=True, validators=[scholarships.validators.validate_ronin]),
        ),
    ]
