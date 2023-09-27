from pprint import pprint

from oncall_client.client import OncallClient
from oncall_client.deps import get_container


def main():
    client: OncallClient = get_container().resolve(OncallClient)
    client.login()

    pprint(client.get_user(username='irusland'))


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    main()
