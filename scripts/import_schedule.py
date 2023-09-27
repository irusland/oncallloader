from pydantic_yaml import parse_yaml_raw_as
import uuid
from datetime import datetime, timedelta
from pprint import pprint

from oncall_client.client import OncallClient, CreateTeamRequest, CreateEventRequest, \
    UpdateUserRequest, Contacts, Role
from oncall_client.deps import get_container
from pydantic import BaseModel, field_validator

from dateutil.parser import parse


class DutySchedule(BaseModel):
    date: datetime
    role: Role

    @field_validator("date", mode='before')
    @classmethod
    def _normalize_date(cls, v) -> datetime:
        return parse(v)


class UserSchedule(BaseModel):
    name: str
    full_name: str
    phone_number: str
    email: str
    duty: list[DutySchedule]


class TeamSchedule(BaseModel):
    name: str
    scheduling_timezone: str
    email: str
    slack_channel: str
    users: list[UserSchedule]


class ImportSchedule(BaseModel):
    teams: list[TeamSchedule]


def main():
    with open('import.yaml', 'r') as f:
        import_schedule = parse_yaml_raw_as(ImportSchedule, f.read())
        pprint(import_schedule.model_dump())

    client: OncallClient = get_container().resolve(OncallClient)
    client.login()

    roster_name = 'main'
    for team in import_schedule.teams:
        try:
            client.create_team(
                request=CreateTeamRequest(
                    name=team.name,
                    scheduling_timezone=team.scheduling_timezone,
                    email=team.email,
                    slack_channel=team.slack_channel,
                )
            )
            client.create_roster(team_name=team.name, roster_name=roster_name)
        except:
            pass
        for user in team.users:
            try:
                client.create_user(
                    request=UpdateUserRequest(
                        contacts=Contacts(
                            email=user.email,
                            sms=user.phone_number,
                            call=user.phone_number,
                            slack=team.slack_channel,
                        ),
                        name=user.name,
                        full_name=user.full_name,
                        time_zone=team.scheduling_timezone,
                        active=1,
                    )
                )
                client.add_user_to_team(
                    team_name=team.name,
                    roster_name=roster_name,
                    user_name=user.name
                )
            except:
                pass
            for duty in user.duty:
                client.create_event(
                    request=CreateEventRequest(
                        start=duty.date,
                        end=duty.date + timedelta(days=1),
                        user=user.name,
                        team=team.name,
                        role=duty.role,
                    )
                )

        pprint(client.get_team(team_name=team.name))


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    main()
