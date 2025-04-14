# Generated by Django 5.2 on 2025-04-14 13:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referrer_id', models.BigIntegerField()),
                ('referred_user_id', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referal_count', models.IntegerField(default=0)),
                ('chat_id', models.BigIntegerField(blank=True, default=0, null=True)),
                ('interface_language', models.CharField(max_length=10)),
                ('photo', models.CharField(blank=True, max_length=255, null=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('role', models.CharField(blank=True, choices=[('ADMIN', 'Admin'), ('USER', 'Foydalanuvchi')], default='USER', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PdfFileId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.user')),
            ],
        ),
        migrations.CreateModel(
            name='Otziv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], max_length=1)),
                ('opinion', models.TextField(blank=True, null=True)),
                ('objection', models.TextField(blank=True, null=True)),
                ('image', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.user')),
            ],
        ),
    ]
