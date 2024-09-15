# Generated by Django 4.2.16 on 2024-09-15 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['order']},
        ),
        migrations.AddIndex(
            model_name='content',
            index=models.Index(fields=['order'], name='courses_con_order_53ec53_idx'),
        ),
        migrations.AddIndex(
            model_name='module',
            index=models.Index(fields=['order'], name='courses_mod_order_e9c068_idx'),
        ),
    ]
