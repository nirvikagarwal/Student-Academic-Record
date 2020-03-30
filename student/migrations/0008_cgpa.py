# Generated by Django 3.0.4 on 2020-03-30 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0007_auto_20200326_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cgpa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cgpa', models.FloatField(null=True)),
                ('semester', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.AllSemester')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
