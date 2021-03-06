# Generated by Django 3.0.4 on 2020-03-25 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AllSemester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('First Semester', 'First Semester'), ('Second Semester', 'Second Semester'), ('Third Semester', 'Third Semester'), ('Fourth Semester', 'Fourth Semester'), ('Fifth Semester', 'Fifth Semester'), ('Sixth Semester', 'Sixth Semester'), ('Seventh Semester', 'Seventh Semester'), ('Eighth Semester', 'Eighth Semester')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AllSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('code', models.CharField(max_length=10, null=True)),
                ('credit_points', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('code', models.CharField(max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.AllSemester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subjects', models.ManyToManyField(to='student.AllSubject')),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(null=True)),
                ('reg', models.CharField(max_length=8, null=True, unique=True, verbose_name='Registration no.')),
                ('roll', models.CharField(max_length=8, null=True, unique=True, verbose_name='Roll no.')),
                ('address', models.TextField(null=True, verbose_name='Address')),
                ('contact', models.CharField(max_length=13, null=True, unique=True)),
                ('photograph', models.ImageField(null=True, upload_to='student/images')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Department')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.FloatField(null=True)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.AllSemester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.AllSubject')),
            ],
        ),
    ]
