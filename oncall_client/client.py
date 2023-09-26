from oncall_client.settings import OncallSettings
from pydantic import BaseModel
from requests import Session


class Team(BaseModel):
    pass


class OncallClient:
    def __init__(self, settings: OncallSettings):
        self._settings = settings
        self._session = Session()

    def get_teams(self) -> list[str]:
        response = self._session.get(self._settings.teams_endpoint)
        return response.json()
