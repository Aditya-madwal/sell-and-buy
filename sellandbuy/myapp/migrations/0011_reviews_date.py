# Generated by Django 5.0.4 on 2024-05-06 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_reviews_stars'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
