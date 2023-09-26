from pydantic import SecretStr
from pydantic_settings import BaseSettings


class OncallSettings(BaseSettings):
    url: str

    username: str
    password: str

    teams_path: str = '/api/v0/teams'
    login_path: str = '/login'

    @property
    def teams_endpoint(self) -> str:
        return self.url + self.teams_path

    @property
    def login_endpoint(self) -> str:
        return self.url + self.login_path

    class Config:
        env_prefix = 'ONCALL_SETTINGS_'
