from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Serial


ID = "2024-03-25T10:45:17:930697"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="home", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="NewUser",
        tablename="new_user",
        column_name="user_id",
        db_column_name="user_id",
        params={"primary_key": True},
        old_params={"primary_key": False},
        column_class=Serial,
        old_column_class=Serial,
        schema=None,
    )

    return manager
