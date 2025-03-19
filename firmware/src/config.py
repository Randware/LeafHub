import json

CONFIG_PATH: str = "config.json"


class Config:
    def __init__(
        self,
        network_ssid: str,
        network_password: str,
        server_address: str,
        auth_token: str,
    ) -> None:
        self.network_ssid = network_ssid
        self.network_password = network_password
        self.server_address = server_address
        self.auth_token = auth_token

    def save(self) -> None:
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.__dict__, f)


def exists() -> bool:
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)

            Config(**config)
        return True
    except (OSError, ValueError):
        return False


def load() -> Config:
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

        return Config(**config)
