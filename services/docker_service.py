import subprocess

def run_command(command):
    return subprocess.check_output(command, 
    shell=True)

def get_latest(image):
    if not image:
        return run_command('docker ps --format="{{json .}}" -l')
    return run_command(f'docker ps --filter "ancestor={image}" --format="{{{{json .}}}}" -l')

def create(image,detached,publish):
    publish = '--publish-all' if publish is True else f'-p {publish}:80' if publish else ''
    if not detached:
        try:
            subprocess.check_output(f'docker run {publish} {image}',shell=True)
        except subprocess.CalledProcessError:
            return {'error':'Command line error'}
        return 
    detached = '-d' if detached else ''
    try:
        run_command(f'docker run {detached} {publish} {image}')
    except subprocess.CalledProcessError:
        return {'error':'Command line error'}
    return 

def health_check():
    return run_command(f'docker-compose up -d')
