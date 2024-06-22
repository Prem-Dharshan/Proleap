# Generated by Django 5.0.6 on 2024-06-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('SHORT_ANSWER', 'short_answer'), ('PARAGRAPH', 'paragraph'), ('NUMBER', 'number'), ('RADIO', 'radio'), ('DATE', 'date'), ('FILE', 'file'), ('CHECKBOXES', 'checkboxes'), ('URL', 'url'), ('IMAGE', 'image'), ('TIME', 'time'), ('EMAIL', 'email')], default='SHORT_ANSWER', max_length=64),
        ),
    ]