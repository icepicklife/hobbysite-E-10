# Generated by Django 5.1.6 on 2025-05-07 15:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user_management", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Commission",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Open", "Open"),
                            ("Full", "Full"),
                            ("Completed", "Completed"),
                            ("Discontinued", "Discontinued"),
                        ],
                        default="Open",
                        max_length=20,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user_management.profile",
                    ),
                ),
            ],
            options={
                "ordering": ["created_on"],
            },
        ),
        migrations.CreateModel(
            name="Job",
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
                ("role", models.CharField(max_length=255)),
                ("manpower_required", models.PositiveIntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[("Open", "Open"), ("Full", "Full")],
                        default="Open",
                        max_length=20,
                    ),
                ),
                (
                    "commission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="commission.commission",
                    ),
                ),
            ],
            options={
                "ordering": ["status", "-manpower_required", "role"],
            },
        ),
        migrations.CreateModel(
            name="JobApplication",
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
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Accepted", "Accepted"),
                            ("Rejected", "Rejected"),
                        ],
                        default="Pending",
                        max_length=20,
                    ),
                ),
                ("applied_on", models.DateTimeField(auto_now_add=True)),
                (
                    "applicant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user_management.profile",
                    ),
                ),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="commission.job"
                    ),
                ),
            ],
            options={
                "ordering": [
                    models.Case(
                        models.When(status="Pending", then=1),
                        models.When(status="Accepted", then=2),
                        models.When(status="Rejected", then=3),
                        output_field=models.IntegerField(),
                    ),
                    "-applied_on",
                ],
            },
        ),
    ]
