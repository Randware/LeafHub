import webui
from time import sleep
import config
import monitor


EXECUTION_DELAY = 1

if __name__ == "__main__":
    print(f"Starting execution in {EXECUTION_DELAY} second(s) ...\n")
    sleep(EXECUTION_DELAY)

    while True:
        print("Running from entry point ...")

        print("Checking for config ...")
        if config.is_valid():
            print("Valid config detected")

            try:
                monitor.start()
            except Exception as e:
                print(e)
                print("Monitoring failed, entering configuration mode ...")
                webui.start()
        else:
            print("No valid config detected")
            print("Starting configuration mode ...")
            webui.start()

