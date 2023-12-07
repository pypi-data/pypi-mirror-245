# Generated by Django 3.2.12 on 2022-02-21 13:05
from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import migrations

if TYPE_CHECKING:
    from django.apps.registry import Apps
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor

ROLES = [
    {
        "name": "EDITOR",
        "add_permissions": [
            "publish_event",
        ],
        "remove_permissions": [
            "change_feedback",
            "change_imprintpage",
            "view_feedback",
            "view_imprintpage",
        ],
    },
    {
        "name": "EVENT_MANAGER",
        "add_permissions": [],
        "remove_permissions": [
            "change_feedback",
            "view_feedback",
            "view_imprintpage",
        ],
    },
]


# pylint: disable=unused-argument
def update_roles(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    """
    Update the permissions of roles

    :param apps: The configuration of installed applications
    :param schema_editor: The database abstraction layer that creates actual SQL code
    """
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    for role_conf in ROLES:
        group = Group.objects.get(name=role_conf.get("name"))
        add_permissions = Permission.objects.filter(
            codename__in=role_conf.get("add_permissions")
        )
        group.permissions.add(*add_permissions)
        remove_permissions = Permission.objects.filter(
            codename__in=role_conf.get("remove_permissions")
        )
        group.permissions.remove(*remove_permissions)


# pylint: disable=unused-argument
def revert_roles(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    """
    Revert the permission changes of this migration

    :param apps: The configuration of installed applications
    :param schema_editor: The database abstraction layer that creates actual SQL code
    """
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    for role_conf in ROLES:
        group = Group.objects.get(name=role_conf.get("name"))
        # The permissions that were added with this migration need to be removed
        add_permissions = Permission.objects.filter(
            codename__in=role_conf.get("add_permissions")
        )
        group.permissions.remove(*add_permissions)
        # The migrations that were removed with this migration need to be added again
        remove_permissions = Permission.objects.filter(
            codename__in=role_conf.get("remove_permissions")
        )
        group.permissions.add(*remove_permissions)


class Migration(migrations.Migration):
    """
    Migration file to update permissions of roles
    """

    dependencies = [
        ("cms", "0006_region_custom_prefix"),
    ]

    operations = [
        migrations.RunPython(update_roles, revert_roles),
    ]
