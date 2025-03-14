from webui import start
from time import sleep

EXECUTION_DELAY = 1

# Start the server when the script runs
if __name__ == "__main__":
    print(f"Starting execution in {EXECUTION_DELAY} second(s) ...\n")
    sleep(EXECUTION_DELAY)
    start()
