# Generated by Django 2.1.7 on 2019-08-10 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file_handle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('file_recepient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recepient', to='file_handle.CustomUser')),
                ('file_uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploader', to='file_handle.CustomUser')),
            ],
        ),
    ]
