from oncall_client.client import OncallClient
from oncall_client.settings import OncallSettings
from punq import Container, Scope


def get_container() -> Container:
    container = Container()
    container.register(OncallSettings, lambda: OncallSettings(), scope=Scope.singleton)
    container.register(OncallClient, OncallClient, scope=Scope.singleton)
    return container
