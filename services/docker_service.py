import subprocess, logging

def run_command(command):
    return subprocess.check_output(command, 
    shell=True)

def get_all():
    return run_command("echo ] | (docker ps -a --format '{{json .}}' | paste -sd',' && cat) | (echo [ && cat)")

def get_latest(image):
    if not image:
        return run_command('docker ps --format="{{json .}}" -l')
    return run_command(f'docker ps --filter "ancestor={image}" --format="{{{{json .}}}}" -l')

def create(image,detached,publish):
    publish = '--publish-all' if publish is True else f'-p {publish}:80' if publish else ''
    if not detached:
        try:
            run_command(f'docker run {publish} {image}')
        except subprocess.CalledProcessError:
            return {'error':'Command line error'}
        return 
    detached = '-d' if detached else ''
    try:
        run_command(f'docker run {detached} {publish} {image}')
    except subprocess.CalledProcessError:
        return {'error':'Command line error'}
    return 

def periodic_check():

    run_command('docker-compose up -d')
    #config_services =  run_command('docker-compose ps -q').decode("utf-8").split()
    #running_services = run_command('docker inspect --format "{{.Id}}" $(docker ps -q)').decode("utf-8").split()

 #   for i in running_services:
 #       if i not in config_services:
 #           run_command(f'docker stop {i}')
 #           print('Killed service',i) 
