from oncall_client.client import OncallClient, CreateTeamRequest, LoginRequest
from oncall_client.deps import get_container


def main():
    client: OncallClient = get_container().resolve(OncallClient)
    print(client.login())


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    main()
