# Generated by Django 3.2.12 on 2022-03-04 21:19

from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    """
    Migration file to change the ordering of translation models
    (additionally order translation objects by language)
    """

    dependencies = [
        ("cms", "0008_alter_pushnotification_channel"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="eventtranslation",
            options={
                "default_permissions": (),
                "default_related_name": "event_translations",
                "ordering": ["event__pk", "language__pk", "-version"],
                "verbose_name": "event translation",
                "verbose_name_plural": "event translations",
            },
        ),
        migrations.AlterModelOptions(
            name="imprintpagetranslation",
            options={
                "default_permissions": (),
                "default_related_name": "imprint_translations",
                "ordering": ["page__pk", "language__pk", "-version"],
                "verbose_name": "imprint translation",
                "verbose_name_plural": "imprint translations",
            },
        ),
        migrations.AlterModelOptions(
            name="pagetranslation",
            options={
                "default_permissions": (),
                "default_related_name": "page_translations",
                "ordering": ["page__pk", "language__pk", "-version"],
                "verbose_name": "page translation",
                "verbose_name_plural": "page translations",
            },
        ),
        migrations.AlterModelOptions(
            name="poitranslation",
            options={
                "default_permissions": (),
                "default_related_name": "poi_translations",
                "ordering": ["poi__pk", "language__pk", "-version"],
                "verbose_name": "location translation",
                "verbose_name_plural": "location translations",
            },
        ),
        migrations.AlterModelOptions(
            name="pushnotificationtranslation",
            options={
                "default_permissions": (),
                "ordering": ["push_notification__pk", "language__pk", "language"],
                "verbose_name": "push notification translation",
                "verbose_name_plural": "push notification translations",
            },
        ),
    ]
