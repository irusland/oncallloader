from oncall_client.client import OncallClient
from oncall_client.deps import get_container


def main():
    client = get_container().resolve(OncallClient)
    print(client.get_teams())


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    main()
