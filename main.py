if __name__ == "__main__":
    import asyncio

    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    from app import app

    class CustomConfig(Config):
        use_reloader = True
        _bind = ["127.0.0.1:8080"]
    asyncio.run(serve(app, CustomConfig()))

    serve(app)
