# Generated by Django 3.0.2 on 2020-01-06 00:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20200105_0945'),
    ]

    operations = [
        migrations.CreateModel(
            name='CannedMessage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('body', models.TextField(max_length=500)),
                ('category', models.TextField(choices=[('undetermined', 'Undetermined'), ('apology', 'Apologize'), ('greeting', 'Greet'), ('thank', 'Thank'), ('wait', 'Wait')], default='undetermined', max_length=140)),
            ],
        ),
    ]
