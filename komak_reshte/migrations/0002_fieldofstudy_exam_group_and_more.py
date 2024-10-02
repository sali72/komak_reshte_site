# Generated by Django 5.1 on 2024-10-02 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('komak_reshte', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldofstudy',
            name='exam_group',
            field=models.CharField(default='tajrobi', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='enrollmentdata',
            name='extra_information',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='fieldofstudy',
            name='unique_code',
            field=models.IntegerField(max_length=50, unique=True),
        ),
    ]
