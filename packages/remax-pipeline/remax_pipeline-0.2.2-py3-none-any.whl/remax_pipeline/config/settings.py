from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings


class Base(BaseSettings):
    class Config:
        env_file = find_dotenv()
        load_dotenv(env_file)


class CelerySettings(Base):
    rabbitmq_broker: str
    app_name: str

    class Config:
        env_prefix = "CELERY_"


class PostegresSettings(Base):
    dbname: str
    user: str
    password: str
    host: str
    port: str

    class Config:
        env_prefix = "POSTGRES_"
