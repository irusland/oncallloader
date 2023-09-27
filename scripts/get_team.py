from pprint import pprint

from oncall_client.client import OncallClient
from oncall_client.deps import get_container


def main():
    client = get_container().resolve(OncallClient)
    pprint(client.get_team(team_name='Test Team'))


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    main()
