from pydantic import SecretStr
from pydantic_settings import BaseSettings


class OncallSettings(BaseSettings):
    url: str

    username: str
    password: str

    teams_path: str = '/api/v0/teams'
    login_path: str = '/login'
    users_path: str = '/api/v0/users'
    events_path: str = '/api/v0/events'

    @property
    def teams_endpoint(self) -> str:
        return self.url + self.teams_path

    @property
    def login_endpoint(self) -> str:
        return self.url + self.login_path

    @property
    def users_endpoint(self) -> str:
        return self.url + self.users_path

    @property
    def events_endpoint(self) -> str:
        return self.url + self.events_path

    class Config:
        env_prefix = 'ONCALL_SETTINGS_'
