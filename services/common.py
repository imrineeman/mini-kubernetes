import json,subprocess

def json_parser(data):
    try:
        parsed_data = json.loads(data)
    except json.JSONDecodeError:
        return {'error':'JSON decode error'}
    return parsed_data

def run_command(command):
    return subprocess.check_output(command, shell=True)