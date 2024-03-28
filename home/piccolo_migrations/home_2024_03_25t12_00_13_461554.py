from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Varchar


ID = "2024-03-25T12:00:13:461554"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="home", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="NewUser",
        tablename="new_user",
        column_name="user_name",
        db_column_name="user_name",
        params={"unique": True},
        old_params={"unique": False},
        column_class=Varchar,
        old_column_class=Varchar,
        schema=None,
    )

    return manager
