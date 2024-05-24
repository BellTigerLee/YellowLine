# Generated by Django 5.0.3 on 2024-05-09 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=45)),
                ('name', models.CharField(max_length=45)),
                ('option', models.CharField(choices=[('Protector', '보호자'), ('Protected', '피보호자')], max_length=45)),
                ('phoneNum', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('historyNum', models.AutoField(primary_key=True, serialize=False)),
                ('departure', models.CharField(max_length=45)),
                ('arrival', models.CharField(max_length=45)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserRelation',
            fields=[
                ('userRelationNum', models.AutoField(primary_key=True, serialize=False)),
                ('helper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='helper_set', to='DB.user')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_set', to='DB.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserState',
            fields=[
                ('userStateNum', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.CharField(choices=[('Offline', '오프라인'), ('Walking', '도보'), ('Navigation', '네비게이션')], max_length=45)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.user')),
            ],
        ),
    ]