import uuid
from pprint import pprint

from oncall_client.client import OncallClient, CreateTeamRequest
from oncall_client.deps import get_container


def main():
    client: OncallClient = get_container().resolve(OncallClient)
    client.login()
    team_name = 'teamname' + uuid.uuid1().hex
    client.create_team(
        request=CreateTeamRequest(
            name=team_name,
            scheduling_timezone="US/Pacific",
            email='irusland@tinkoff.ru',
            slack_channel='#brainstorming',
        )
    )
    client.create_roster(team_name=team_name, roster_name='Main')
    pprint(client.get_team(team_name=team_name))


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    main()
