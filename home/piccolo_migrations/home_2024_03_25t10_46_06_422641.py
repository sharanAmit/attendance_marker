from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2024-03-25T10:46:06:422641"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="home", description=DESCRIPTION
    )

    manager.drop_column(
        table_class_name="NewUser",
        tablename="new_user",
        column_name="user_id",
        db_column_name="user_id",
        schema=None,
    )

    return manager
