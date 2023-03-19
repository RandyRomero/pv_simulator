import os


class Settings:
    # rabbit
    RABBIT_HOST = os.environ.get("RABBIT_HOST", "localhost")
    RABBIT_PORT = int(os.environ.get("RABBIT_PORT", 5672))
    RABBIT_LOGIN = os.environ.get("RABBIT_LOGIN", "guest")
    RABBIT_PASSWORD = os.environ.get("RABBIT_PASSWORD", "guest")


settings = Settings
