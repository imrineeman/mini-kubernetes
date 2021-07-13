import subprocess
def run_command(command):
    return subprocess.check_output(command, 
    shell=True)

def get_latest(image):
    if not image:
        return run_command('docker ps --format="{{json .}}" -l')
    return run_command(f'docker ps --filter "ancestor={image}" --format="{{{{json .}}}}" -l')

def create(image):
    try:
        run_command(f'docker run {image}')
    except subprocess.CalledProcessError:
        return {'error':'Image not found'}
    return ''