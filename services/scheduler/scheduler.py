import requests,sys,time

def main():
    CONTROLLER_BASE_URL = sys.argv[1]
    CONTROLLER_PORT = sys.argv[2]
    SCHEDULER_INTERVALS = int(sys.argv[3])
    while True:
        BASE_URL = f'http://{CONTROLLER_BASE_URL}:{CONTROLLER_PORT}'
        requests.put(f'{BASE_URL}/services')
        requests.delete(f'{BASE_URL}/services')
        time.sleep(SCHEDULER_INTERVALS)

if __name__ == '__main__':
    main()
    