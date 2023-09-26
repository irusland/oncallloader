import os

from pydantic_settings import BaseSettings


class OncallSettings(BaseSettings):
    url: str
    teams_path: str = '/api/v0/teams'

    @property
    def teams_endpoint(self) -> str:
        return self.url + self.teams_path

    class Config:
        env_prefix = 'ONCALL_SETTINGS_'
