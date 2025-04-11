import webui
from time import sleep
import config
import monitor
import machine

EXECUTION_DELAY = 1

def configure_flow():
    print("Entering configuration flow ...")

    print("Starting configuration webui ...")
    webui.start()

    print("Restarting ...")
    machine.reset()

if __name__ == "__main__":
    print(f"Starting execution in {EXECUTION_DELAY} second(s) ...\n")
    sleep(EXECUTION_DELAY)

    print("Running from entry point ...")

    print("Checking for config ...")

    if config.is_valid():
        print("Valid config detected")

        try:
            monitor.start()
        except Exception as e:
            print(e)
            print("Monitoring failed unexpectedly")
            configure_flow()
    else:
        print("No valid config detected")
        configure_flow()

