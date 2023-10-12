import uuid
from datetime import datetime, timedelta
from pprint import pprint

from oncall_client.client import OncallClient, CreateTeamRequest, CreateEventRequest, \
    UpdateUserRequest, Contacts, Role
from oncall_client.deps import get_container


def main():
    client: OncallClient = get_container().resolve(OncallClient)
    pprint(client.login())

    pprint(
        client.search_events(
            team='k8s SRE',
            start_date=datetime.now(),
        )
    )


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    main()
