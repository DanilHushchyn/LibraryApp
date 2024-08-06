# Generated by Django 5.0.7 on 2024-07-31 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_options_customuser_is_librarian_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LibraryVisitor',
            new_name='Visitor',
        ),
        migrations.AlterModelOptions(
            name='visitor',
            options={'ordering': ['-user__date_joined'], 'verbose_name': 'Visitor', 'verbose_name_plural': 'Visitors'},
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='is_library_visitor',
            new_name='is_visitor',
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='custom_users',
        ),
        migrations.AlterModelTable(
            name='librarian',
            table='librarians',
        ),
        migrations.AlterModelTable(
            name='visitor',
            table='visitors',
        ),
    ]