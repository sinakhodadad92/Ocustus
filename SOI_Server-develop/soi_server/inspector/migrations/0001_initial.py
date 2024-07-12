# Generated by Django 3.2.9 on 2022-01-07 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_state', models.CharField(choices=[('P', 'In_progress'), ('F', 'Failed'), ('C', 'Completed')], default='P', max_length=1)),
                ('name', models.CharField(max_length=50)),
                ('config', models.FileField(upload_to='data/configs/')),
                ('position', models.FileField(upload_to='data/positions/')),
            ],
        ),
        migrations.CreateModel(
            name='Panel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('panel_photo', models.ImageField(upload_to='data/panel_images/')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='panels', to='inspector.job')),
            ],
        ),
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designator', models.CharField(max_length=50)),
                ('helpful', models.BooleanField(default=True)),
                ('coordinate_x', models.IntegerField(null=True)),
                ('coordinate_y', models.IntegerField(null=True)),
                ('component_image', models.ImageField(upload_to='data/component_errors/')),
                ('component_name', models.CharField(max_length=100, null=True)),
                ('board_id', models.IntegerField()),
                ('panel_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspector.panel')),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_image', models.ImageField(upload_to='data/boards/')),
                ('panel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspector.panel')),
            ],
        ),
    ]
