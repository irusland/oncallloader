from datetime import datetime
from enum import Enum
from functools import wraps
from http import HTTPStatus
from http.client import HTTPException
from pprint import pprint
from typing import Any, Callable

import requests.exceptions

from exporter.metrics_collector import MetricsCollector
from oncall_client.settings import OncallSettings
from pydantic import BaseModel, SecretStr
from requests import Session


class LoginRequest(BaseModel):
    username: str
    password: str


class Contacts(BaseModel):
    email: str | None = None
    sms: str | None = None
    call: str | None = None
    slack: str | None = None


class UpdateUserRequest(BaseModel):
    contacts: Contacts | None = None
    name: str | None = None
    full_name: str | None = None
    time_zone: str | None = None
    photo_url: str | None = None
    active: int | None = None


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


def convert_datetime_to_seconds(date: datetime) -> int:
    return int(date.timestamp())


class Role(str, Enum):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    VACATION = 'vacation'


class CreateEventRequest(BaseModel):
    start: datetime
    end: datetime
    user: str
    team: str
    role: Role

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: convert_datetime_to_seconds
        }


class OncallClient:
    def __init__(self, settings: OncallSettings, metrics_collector: MetricsCollector):
        self._settings = settings
        self._session = Session()
        self._auth_headers = {}
        self._metrics_collector = metrics_collector

        self.login = self._with_status(self.login, self._settings.login_endpoint)
        self.get_teams = self._with_status(self.get_teams, self._settings.teams_endpoint)
        self.get_team = self._with_status(self.get_team, self._settings.teams_endpoint)
        self.search_teams = self._with_status(self.search_teams, self._settings.teams_endpoint)
        self.create_team = self._with_status(self.create_team, self._settings.teams_endpoint)
        self.get_users = self._with_status(self.get_users, self._settings.users_endpoint)
        self.get_user = self._with_status(self.get_user, self._settings.users_endpoint)
        self.create_user = self._with_status(self.create_user, self._settings.users_endpoint)
        self.create_roster = self._with_status(self.create_roster, f'{self._settings.teams_endpoint}/team/rosters')
        self.create_event = self._with_status(self.create_event, self._settings.events_endpoint)
        self.search_events = self._with_status(self.search_events, self._settings.events_endpoint)

    def _with_status(self, method: Callable, path: str) -> Callable:
        @wraps(method)
        def _wrapped(*args, **kwargs):
            try:
                result = method(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                if e.response is None:
                    status = e.__class__.__name__
                else:
                    status = e.response.status_code
                self._metrics_collector.api_request_statuses.labels(path=path, status=status).inc()
                raise e
            else:
                self._metrics_collector.api_request_statuses.labels(path=path, status=HTTPStatus.OK).inc()
                return result
        return _wrapped

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

    def get_team(self, team_name: str) -> dict[str, Any]:
        response = self._session.get(
            f'{self._settings.teams_endpoint}/{team_name}'
        )
        return response.json()

    def search_teams(self, team_name: str) -> list[str]:
        response = self._session.get(
            self._settings.teams_endpoint,
            params={'name__contains': team_name},
        )
        return response.json()

    def create_team(self, request: CreateTeamRequest) -> None:
        response = self._session.post(
            self._settings.teams_endpoint,
            data=request.model_dump_json(),
            headers=self._auth_headers,
        )

        response.raise_for_status()

    def get_users(self) -> list[str]:
        response = self._session.get(
            self._settings.users_endpoint,
            headers=self._auth_headers,
        )
        return response.json()

    def create_user(self, request: UpdateUserRequest):
        username = request.name
        response = self._session.post(
            f'{self._settings.users_endpoint}',
            json={'name': username},
            headers=self._auth_headers,
        )
        response.raise_for_status()
        json = request.model_dump(exclude_unset=True, exclude={'name'})
        response = self._session.put(
            f'{self._settings.users_endpoint}/{username}',
            json=json,
            headers=self._auth_headers,
        )
        response.raise_for_status()

    def get_user(self, username: str) -> list[str]:
        response = self._session.get(
            f'{self._settings.users_endpoint}/{username}',
            headers=self._auth_headers,
        )
        return response.json()

    def create_roster(self, team_name: str, roster_name: str) -> None:
        response = self._session.post(
            f'{self._settings.teams_endpoint}/{team_name}/rosters',
            json={
                "name": roster_name,
            },
        )
        response.raise_for_status()

    def add_user_to_team(self, team_name: str, roster_name: str, user_name: str) -> dict[str, Any]:
        response = self._session.post(
            f'{self._settings.teams_endpoint}/{team_name}/rosters/{roster_name}/users',
            json={
                "name": user_name,
            },
        )
        response.raise_for_status()
        return response.json()

    def create_event(self, request: CreateEventRequest) -> None:
        response = self._session.post(
            self._settings.events_endpoint,
            json=request.model_dump(mode='json'),
        )
        response.raise_for_status()

    def search_events(self, team: str, start_date: datetime) -> dict[str, Any]:
        response = self._session.get(
            self._settings.events_endpoint,
            params={
                'team': team,
                'start__gt': convert_datetime_to_seconds(start_date)
            }
        )
        response.raise_for_status()
        return response.json()
