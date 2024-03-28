from piccolo.columns.defaults.timestamptz import TimestamptzNow
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table
from piccolo.columns import Varchar, Boolean, Serial, Text, Timestamptz, ForeignKey, OnDelete, OnUpdate


class Task(Table):
    """
    An example table.
    """
    id: Serial
    name = Varchar()
    completed = Boolean(default=False)


class NewUser(Table):
    first_name = Varchar(null=False, required=True)
    last_name = Varchar(null=False, required=True)
    id: Serial
    user_image = Text(null=False, required=True)
    user_name = Varchar(null=False, required=True, unique=True)
    password = Varchar(null=False, required=True, )
    creation_date = Timestamptz(
        default=TimestamptzNow(),
        null=False,
    )


class Device(Table):
    id: Serial
    device_id = Varchar()
    device_name = Varchar()
    device_OS_name = Varchar()
    device_build_number = Varchar()
    device_finger_print = Varchar()


class DeviceUser(Table):
    device_id = ForeignKey(
        references=Device,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        target_column=None,
        null=True,
        primary_key=False,
        unique=False,
        index=True,
        index_method=IndexMethod.btree,
        db_column_name=None,
        secret=False,
    )
    user_id = ForeignKey(
        references=NewUser,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        target_column=None,
        null=True,
        primary_key=False,
        unique=False,
        index=True,
        index_method=IndexMethod.btree,
        db_column_name=None,
        secret=False,
    )


class Attendance(Table):
    id: Serial
    user_id = ForeignKey(
        references=NewUser,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        target_column=None,
        null=True,
        primary_key=False,
        unique=False,
        index=True,
        index_method=IndexMethod.btree,
        db_column_name=None,
        secret=False,
    )
    check_in_latitude = Varchar()
    check_in_longitude = Varchar()
    check_in_address = Varchar()
    check_in_date = Timestamptz(
        default=TimestamptzNow(),
        null=False,
    )
    check_out_latitude = Varchar()
    check_out_longitude = Varchar()
    check_out_address = Varchar()
    check_out_date = Timestamptz(
        default=TimestamptzNow(),
        null=False,
    )
    device_id = ForeignKey(
        references=Device,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        target_column=None,
        null=True,
        primary_key=False,
        unique=False,
        index=True,
        index_method=IndexMethod.btree,
        db_column_name=None,
        secret=False,
    )
    clock_in_time = Timestamptz(
        default=TimestamptzNow(),
        null=False,
    )
    clock_out_time = Timestamptz()


class Firm(Table):
    id: Serial
    firm_name = Varchar()
    firm_image = Text()
    contact_number = Varchar()
    mail_address = Varchar()
    firm_address = Varchar()
    firm_latitude = Varchar()
    firm_longitude = Varchar()
    firm_type = Varchar()



class Post(Table):
    id: Serial
    title = Varchar()
    image = Text()
    caption = Varchar()
    content = Varchar()
    postedBy = ForeignKey(
        references=NewUser,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.no_action,
        target_column=None,
        null=True,
        primary_key=False,
        unique=False,
        index=True,
        index_method=IndexMethod.btree,
        db_column_name=None,
        secret=False,
    )
    creation_date = Timestamptz(
        default=TimestamptzNow(),
        null=False,
    )
    location = Varchar()
