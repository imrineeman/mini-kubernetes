import requests,sys,time

while True:
    time.sleep(SCHEDULER_INTERVALS)
    CONTROLLER_BASE_URL = sys.argv[1]
    CONTROLLER_PORT = sys.argv[2]
    SCHEDULER_INTERVALS = int(sys.argv[3])

    BASE_URL = f'http://{CONTROLLER_BASE_URL}:{CONTROLLER_PORT}'

    periodic_check= requests.get(f'{BASE_URL}/config')
    remove_unwanted_services= requests.get(f'{BASE_URL}/config/refresh')
