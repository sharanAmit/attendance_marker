from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Timestamptz
from piccolo.columns.column_types import Varchar
from piccolo.columns.defaults.timestamptz import TimestamptzNow
from piccolo.columns.indexes import IndexMethod


ID = "2024-03-28T21:36:37:261770"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="home", description=DESCRIPTION
    )

    manager.add_column(
        table_class_name="Attendance",
        tablename="attendance",
        column_name="check_out_address",
        db_column_name="check_out_address",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Attendance",
        tablename="attendance",
        column_name="check_out_date",
        db_column_name="check_out_date",
        column_class_name="Timestamptz",
        column_class=Timestamptz,
        params={
            "default": TimestamptzNow(),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Attendance",
        tablename="attendance",
        column_name="check_out_latitude",
        db_column_name="check_out_latitude",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Attendance",
        tablename="attendance",
        column_name="check_out_longitude",
        db_column_name="check_out_longitude",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.rename_column(
        table_class_name="Attendance",
        tablename="attendance",
        old_column_name="attendance_address",
        new_column_name="check_in_address",
        old_db_column_name="attendance_address",
        new_db_column_name="check_in_address",
        schema=None,
    )

    manager.rename_column(
        table_class_name="Attendance",
        tablename="attendance",
        old_column_name="attendance_date",
        new_column_name="check_in_date",
        old_db_column_name="attendance_date",
        new_db_column_name="check_in_date",
        schema=None,
    )

    manager.rename_column(
        table_class_name="Attendance",
        tablename="attendance",
        old_column_name="attendance_latitude",
        new_column_name="check_in_latitude",
        old_db_column_name="attendance_latitude",
        new_db_column_name="check_in_latitude",
        schema=None,
    )

    manager.rename_column(
        table_class_name="Attendance",
        tablename="attendance",
        old_column_name="attendance_longitude",
        new_column_name="check_in_longitude",
        old_db_column_name="attendance_longitude",
        new_db_column_name="check_in_longitude",
        schema=None,
    )

    return manager
