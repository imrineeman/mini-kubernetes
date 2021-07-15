import subprocess,sys
from common import json_parser,run_command, SCHEDULER_IMAGE

def get_all():
    data = json_parser(
        run_command(
            "echo ] | (docker ps -a --format '{{json .}}' | paste -sd',' && cat) | (echo [ && cat)"))
    return data

def get_latest(image):
    if not image:
        return json_parser(
            run_command('docker ps --format="{{json .}}" -l'))
    return json_parser(
        run_command(
            f'docker ps --filter "ancestor={image}" --format="{{{{json .}}}}" -l'))

def create(image,publish):
    publish = '--publish-all' if publish is True else f'-p {publish}:80' if publish else ''
    try:
        run_command(f'docker run -d {publish} {image}')
    except subprocess.CalledProcessError:
        return {'error':'Command line error'}
    return {'body': 'Successfuly created'}

def remove_unwanted_services():
    try:
        config_services =  run_command(
            f'docker-compose ps -q').decode("utf-8").split()
        running_services = run_command(
            'docker inspect --format "{{.Id}}" $(docker ps -q)').decode("utf-8").split()
        CONTROLLER_CONTAINER_ID = run_command(
            'docker inspect --format "{{.Id}}" $(cat /etc/hostname)').decode("utf-8").rstrip()
        SCHEDULER_CONTAINER_ID = run_command(f'docker inspect --format="{{{{.Id}}}}" $(docker ps --filter "ancestor={SCHEDULER_IMAGE}" -q)').decode("utf-8").rstrip()
        
        config_services.append(CONTROLLER_CONTAINER_ID)
        config_services.append(SCHEDULER_CONTAINER_ID)

        for service in running_services:
            if service not in config_services:
                run_command(f'docker kill {service}')
                
    except subprocess.CalledProcessError:
        return {'error':'Command line error'}
    return {'status':'Refreshed services'}

def ensure_services_alive():
    run_command('docker-compose up -d')
    return {'status':'Vital services are up'}
