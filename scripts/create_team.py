from oncall_client.client import OncallClient, CreateTeamRequest
from oncall_client.deps import get_container


def main():
    client: OncallClient = get_container().resolve(OncallClient)
    client.login()
    client.create_team(
        request=CreateTeamRequest(
            name='irusland',
            scheduling_timezone="US/Pacific",
            email='irusland@tinkoff.ru',
            slack_channel='#brainstorming',
        )
    )


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    main()
