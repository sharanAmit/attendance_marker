from piccolo.engine.postgres import PostgresEngine

from piccolo.conf.apps import AppRegistry


DB = PostgresEngine(
    config={
        "database": "duco1",
        "user": "duco_user1",
        "password": "amit_sharan",
        "host": "18.222.43.71",
        "port": 2473,
    }
)

APP_REGISTRY = AppRegistry(
    apps=["home.piccolo_app", "piccolo_admin.piccolo_app"]
)
