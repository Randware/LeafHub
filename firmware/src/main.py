import webui
from time import sleep
import config

EXECUTION_DELAY = 1

if __name__ == "__main__":
    print(f"Starting execution in {EXECUTION_DELAY} second(s) ...\n")
    sleep(EXECUTION_DELAY)

    print("Checking for config ...")
    if config.exists():
        print("Valid config detected")
        conf = config.load()
        print(conf.__dict__)
    else:
        print("No valid config detected")
        print("Starting configuration mode ...")
        conf = config.Config(
            "SSID", "PASSWORD", "server_addr_12345", "token_1234567890"
        )
        conf.save()
        webui.start()
