import uuid
from datetime import datetime, timedelta
from pprint import pprint

from oncall_client.client import OncallClient, CreateTeamRequest, CreateEventRequest, \
    UpdateUserRequest, Contacts, Role
from oncall_client.deps import get_container


def main():
    client: OncallClient = get_container().resolve(OncallClient)
    pprint(client.login())

    team_name = 'teamname' + uuid.uuid1().hex
    user_name = 'irusland-' + uuid.uuid1().hex
    roster_name = 'main'
    client.create_user(
        request=UpdateUserRequest(
            contacts=Contacts(
                email='irusland@tinkoff.ru',
                sms="+1 111-111-1111",
                call="+1 111-111-1111",
                slack='#shanel',
            ),
            name=user_name,
            full_name='Rusland',
            time_zone='US/Pacific',
            photo_url='',
            active=1,
        )
    )
    pprint(client.get_user(username=user_name))
    client.create_team(
        request=CreateTeamRequest(
            name=team_name,
            scheduling_timezone="US/Pacific",
            email='irusland@tinkoff.ru',
            slack_channel='#brainstorming',
        )
    )
    client.create_roster(team_name=team_name, roster_name=roster_name)
    client.add_user_to_team(team_name=team_name, roster_name=roster_name, user_name=user_name)
    client.create_event(request=CreateEventRequest(
        start=datetime.now(),
        end=datetime.now()+timedelta(hours=2),
        user=user_name,
        team=team_name,
        role=Role.PRIMARY,
    ))
    pprint(client.get_team(team_name=team_name))


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    main()
