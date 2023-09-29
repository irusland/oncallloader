import uuid
from pprint import pprint

from oncall_client.client import OncallClient, UpdateUserRequest, Contacts
from oncall_client.deps import get_container


def main():
    client: OncallClient = get_container().resolve(OncallClient)
    client.login()
    name = 'irusland-' + uuid.uuid1().hex
    client.create_user(
        request=UpdateUserRequest(
            contacts=Contacts(
                email='irusland@tinkoff.ru',
                sms="+1 111-111-1111",
                call="+1 111-111-1111",
                slack='#shanel',
            ),
            name=name,
            full_name='Rusland',
            time_zone='US/Pacific',
            photo_url='',
            active=1,
        )
    )
    pprint(client.get_user(username=name))


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    main()
