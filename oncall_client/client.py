from oncall_client.settings import OncallSettings
from pydantic import BaseModel, SecretStr
from requests import Session


class LoginRequest(BaseModel):
    username: str
    password: str


class Contacts(BaseModel):
    email: str
    sms: str
    call: str
    slack: str


class LoginResponse(BaseModel):
    id: int
    name: str
    full_name: str
    time_zone: str | None
    photo_url: str | None
    active: int
    god: int
    contacts: Contacts
    csrf_token: str


class CreateTeamRequest(BaseModel):
    name: str
    scheduling_timezone: str
    email: str
    slack_channel: str


class OncallClient:
    def __init__(self, settings: OncallSettings):
        self._settings = settings
        self._session = Session()
        self._auth_headers = {}

    def login(self) -> LoginResponse:
        request = LoginRequest(
            username=self._settings.username,
            password=self._settings.password,
        )
        response = self._session.post(
            self._settings.login_endpoint,
            data=request.model_dump(),
        )
        response_model = LoginResponse.model_validate(response.json())
        x_csrf_token = response_model.csrf_token
        self._auth_headers['x-csrf-token'] = x_csrf_token
        return response_model

    def get_teams(self) -> list[str]:
        response = self._session.get(self._settings.teams_endpoint)
        return response.json()

    def create_team(self, request: CreateTeamRequest) -> None:
        response = self._session.post(
            self._settings.teams_endpoint,
            data=request.model_dump_json(),
            headers=self._auth_headers,
        )

        response.raise_for_status()
