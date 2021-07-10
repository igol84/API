from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 7000
    database_url: str = 'sqlite:///./db_blogs.sqlite3'

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration_sec: int = 3600


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
