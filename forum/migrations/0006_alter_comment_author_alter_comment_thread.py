# Generated by Django 5.2 on 2025-05-08 14:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0005_rename_author_forum_comment_author"),
        ("user_management", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="forum_comments",
                to="user_management.profile",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="thread",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="forum_comments",
                to="forum.thread",
            ),
        ),
    ]
