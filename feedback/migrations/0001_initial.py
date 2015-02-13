# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('image', models.FileField(default=b'/images/noImage.jpg', upload_to=b'/images/')),
                ('courses', models.ManyToManyField(to='feedback.Courses')),
                ('dept', models.ForeignKey(to='feedback.Department')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feedback', models.IntegerField(default=0)),
                ('course', models.ForeignKey(to='feedback.Courses')),
                ('faculty', models.ForeignKey(to='feedback.Faculty')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeedStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.FloatField(default=0.0)),
                ('course', models.ForeignKey(to='feedback.Courses')),
                ('faculty', models.ForeignKey(to='feedback.Faculty')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('courses', models.ManyToManyField(to='feedback.Courses')),
                ('dept', models.ForeignKey(to='feedback.Department')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='feedstatus',
            name='student',
            field=models.ForeignKey(to='feedback.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedback',
            name='question',
            field=models.ForeignKey(to='feedback.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedback',
            name='student',
            field=models.ForeignKey(to='feedback.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faculty',
            name='question',
            field=models.ManyToManyField(to='feedback.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faculty',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='courses',
            name='dept',
            field=models.ForeignKey(to='feedback.Department'),
            preserve_default=True,
        ),
    ]
