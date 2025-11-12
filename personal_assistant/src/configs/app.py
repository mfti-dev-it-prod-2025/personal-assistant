from dynaconf import Dynaconf
from pydantic import BaseModel


class APPConfig(BaseModel):
    app_host: str
    app_port: int
    app_use_testcontainers: bool = False


class DBConfig(BaseModel):
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

    @property
    def dsl(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


class TestConfig(BaseModel):
    use_testcontainers: bool = False


class JWTConfig(BaseModel):
    jwt_secret: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    jwt_bypass_auth: bool = False


class Settings(BaseModel):
    app: APPConfig
    db: DBConfig
    jwt: JWTConfig


env_settings = Dynaconf(settings_file=["settings.toml"])

settings = Settings(
    app=env_settings["app_settings"],
    db=env_settings["db_settings"],
    jwt=env_settings["jwt_settings"],
)


if __name__ == "__main__":
    print(settings.db.dsl)
