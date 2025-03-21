import json

CONFIG_PATH: str = "config.json"


class Config:
    def __init__(
        self,
        network_ssid: str | None = None,
        network_password: str | None = None,
        server_address: str | None = None,
        auth_token: str | None = None,
    ) -> None:
        self.network_ssid = network_ssid
        self.network_password = network_password
        self.server_address = server_address
        self.auth_token = auth_token

    def save(self) -> None:
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.__dict__, f)


def is_valid() -> bool:
    try:
        with open(CONFIG_PATH, "r") as f:
            config: dict = json.load(f)

            c: Config = Config(**config)

            for _, value in c.__dict__.items():
                if value is None or value == "":
                    return False

        return True
    except (OSError, ValueError, TypeError):
        return False


def load() -> Config:
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)

            return Config(**config)
    except OSError:
        return Config()
