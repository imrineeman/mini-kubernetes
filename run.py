import os, webbrowser, subprocess, sys
from dotenv import load_dotenv
import logging

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"),
              logging.StreamHandler()])


def main():
    # Load environment Variables
    logging.info("Loading env variables")
    load_dotenv()
    
    PORT = os.getenv('CONTROLLER_PORT')
    INTERVAL = os.getenv('SCHEDULER_INTERVALS')
    CONTROLLER_IMAGE = os.getenv('CONTROLLER_IMAGE')
    SCHEDULER_IMAGE = os.getenv('SCHEDULER_IMAGE')

    # Services image build
    logging.info("Building services images")
    try:
        subprocess.check_output(
            f'docker build -t {CONTROLLER_IMAGE} ./services/controller',
            shell=True)
        subprocess.check_output(
            f'docker build -t {SCHEDULER_IMAGE} ./services/scheduler',
            shell=True)
    except subprocess.CalledProcessError:
        logging.warning('Error building images')
    logging.info("Successfuly built images")

    # Install deps
    subprocess.check_output(f'pip3 install -r requirements.txt', shell=True)

    # Run controller service
    logging.info("Running controller service")
    try:
        controller_container_id = subprocess.check_output(
            f'docker run -d -e SCHEDULER_IMAGE={SCHEDULER_IMAGE} -e CONTROLLER_PORT={PORT} -it -v "/var/run/docker.sock:/var/run/docker.sock:rw" -p {PORT}:80 {CONTROLLER_IMAGE}',
            shell=True).decode("utf-8").strip()
    except subprocess.SubprocessError:
        logging.warning('Error running controller service; is the PORT taken?')
        sys.exit(1)
    logging.info("Controller service running")

    # Get environment variable of controller's container ID
    os.environ['CONTROLLER_CONTAINER_ID'] = controller_container_id
    os.environ['CONTROLLER_BASE_IP'] = subprocess.check_output(
        f'docker inspect -f "{{{{ .NetworkSettings.IPAddress }}}}" {controller_container_id}',
        shell=True).decode("utf-8").strip()
    BASE_IP = os.getenv('CONTROLLER_BASE_IP')

    # Run scheduler service
    logging.info('Run scheduler service')
    try:
        subprocess.check_output(
            f'docker run -d -e CONTROLLER_IP={BASE_IP} -e CONTROLLER_PORT={PORT} -e INTERVAL={INTERVAL} scheduler:latest',
            shell=True)
    except subprocess.SubprocessError:
        logging.warning("Error running scheduler service")
    logging.info(
        f'Scheduler service running, sending reset request every {INTERVAL} seconds'
    )
    logging.info(
        f"To log controller server responses, run docker attach {os.getenv('CONTROLLER_CONTAINER_ID')}"
    )

    # Open browser
    webbrowser.open(
        f"{os.getenv('CONTROLLER_BASE_IP')}:{os.getenv('CONTROLLER_PORT')}")


if __name__ == '__main__':
    main()
