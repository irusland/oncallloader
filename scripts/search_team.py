from pprint import pprint

from oncall_client.client import OncallClient
from oncall_client.deps import get_container


def main():
    client = get_container().resolve(OncallClient)
    pprint(client.search_teams(team_name='k8s'))


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    main()
