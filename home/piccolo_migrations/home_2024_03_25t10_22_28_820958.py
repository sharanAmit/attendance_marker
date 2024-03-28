from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2024-03-25T10:22:28:820958"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="home", description=DESCRIPTION
    )

    manager.rename_table(
        old_class_name="User",
        old_tablename="user",
        new_class_name="NewUser",
        new_tablename="new_user",
        schema=None,
    )

    return manager
