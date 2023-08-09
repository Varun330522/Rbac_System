# Generated by Django 4.2.3 on 2023-07-28 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("r_app", "0011_remove_apiusermapping_api_remove_apiusermapping_user_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Action",
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
                ("action_name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="API",
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
                ("api_name", models.CharField(max_length=100, unique=True)),
                ("endpoints", models.TextField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("methods", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Role",
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
                ("role_name", models.CharField(max_length=15, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Users",
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
                ("username", models.CharField(max_length=150, unique=True)),
                ("password", models.CharField(max_length=150)),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="r_app.role"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Token",
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
                ("access", models.TextField()),
                ("refresh", models.TextField()),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="r_app.users"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RoleActionMapping",
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
                (
                    "action",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="r_app.action"
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="r_app.role"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ApiUserMapping",
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
                (
                    "api",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="r_app.api"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="r_app.users"
                    ),
                ),
            ],
        ),
    ]
