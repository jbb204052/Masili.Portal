# Generated by Django 4.1.3 on 2022-11-23 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0002_remove_profile_is_guest_alter_profile_is_resident"),
    ]

    operations = [
        migrations.CreateModel(
            name="Gallery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("caption", models.CharField(blank=True, max_length=50)),
                ("photo", models.ImageField(upload_to=None)),
            ],
        ),
    ]