import os ,webbrowser,subprocess
from dotenv import load_dotenv

# Load environment Variables
load_dotenv()
PORT = os.getenv('CONTROLLER_PORT')
INTERVALS = os.getenv('SCHEDULER_INTERVALS')
CONTROLLER_IMAGE = os.getenv('CONTROLLER_IMAGE')
SCHEDULER_IMAGE = os.getenv('SCHEDULER_IMAGE')

# Run controller service 
controller_container_id = subprocess.check_output(f'docker run -d -e SCHEDULER_IMAGE={SCHEDULER_IMAGE} -it -v "/var/run/docker.sock:/var/run/docker.sock:rw" -p {PORT}:80 {CONTROLLER_IMAGE}' ,shell=True).decode("utf-8").strip()
os.environ['CONTROLLER_CONTAINER_ID'] = controller_container_id
os.environ['CONTROLLER_BASE_IP'] = subprocess.check_output(f'docker inspect -f "{{{{ .NetworkSettings.IPAddress }}}}" {controller_container_id}',shell=True).decode("utf-8").strip()
BASE_IP = os.getenv('CONTROLLER_BASE_IP')

subprocess.check_output(f'docker run -d -e controller_ip={BASE_IP} -e controller_port={PORT} -e interval={INTERVALS} scheduler:latest', shell=True)

# Open browser
webbrowser.open(f"{os.getenv('CONTROLLER_BASE_IP')}:{os.getenv('CONTROLLER_PORT')}")

