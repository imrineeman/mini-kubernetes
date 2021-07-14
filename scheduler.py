import requests,sys,time

if len(sys.argv) < 3:
    print(sys.argv,file=sys.stderr)
    sys.exit(1)
CONTROLLER_BASE_URL = sys.argv[1]
CONTROLLER_PORT = sys.argv[2]
SCHEDULER_INTERVALS = int(sys.argv[3])

while True:

    time.sleep(SCHEDULER_INTERVALS)

    BASE_URL = f'http://{CONTROLLER_BASE_URL}:{CONTROLLER_PORT}'

    periodic_check= requests.get(f'{BASE_URL}/config')
    remove_unwanted_services= requests.get(f'{BASE_URL}/config/reset')
