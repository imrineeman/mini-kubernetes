import json,subprocess,os

# Environment variables passed from host
SCHEDULER_IMAGE = os.getenv('SCHEDULER_IMAGE')

def json_parser(data):
    try:
        parsed_data = json.loads(data)
    except json.JSONDecodeError:
        return {'error':'JSON decode error'}
    return parsed_data

def run_command(command):
    return subprocess.check_output(command, shell=True)