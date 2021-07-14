import subprocess, os
import webbrowser
from dotenv import load_dotenv

load_dotenv()

def run_command(command):
    return subprocess.check_output(command, shell=True)

controller_container_id = run_command('docker run -d -it -v "/var/run/docker.sock:/var/run/docker.sock:rw" -p 5000:80 controller:latest').decode("utf-8").strip()

os.environ['CONTROLLER_CONTAINER_ID'] = controller_container_id
os.environ['CONTROLLER_BASE_URL'] = run_command(f'docker inspect -f "{{{{ .NetworkSettings.IPAddress }}}}" {controller_container_id}').decode("utf-8").strip()

BASE_URL = os.getenv('CONTROLLER_BASE_URL')
PORT = os.getenv('CONTROLLER_PORT')
INTERVALS = os.getenv('SCHEDULER_INTERVALS')

webbrowser.open(f"{os.getenv('CONTROLLER_BASE_URL')}:{os.getenv('CONTROLLER_PORT')}")
run_command(f"python scheduler.py {BASE_URL} {PORT} {INTERVALS} &")
