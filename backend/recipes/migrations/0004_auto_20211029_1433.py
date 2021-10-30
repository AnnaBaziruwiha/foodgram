# Generated by Django 3.2.8 on 2021-10-29 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20211029_0944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientamount',
            old_name='ingredient',
            new_name='item',
        ),
        migrations.AlterUniqueTogether(
            name='ingredientamount',
            unique_together={('item', 'recipe')},
        ),
    ]
