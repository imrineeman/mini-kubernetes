from json.decoder import JSONDecodeError
from flask import Flask , request, jsonify
from services import docker
import json
from flask_apscheduler import APScheduler

app = Flask(__name__)

# Services health check logic
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
INTERVAL_TASK_ID = 'interval-task-id'

#Homepage
@app.route("/")
def homepage():
    return "Mini-Kubernetes!"

# Get all services
@app.route('/services')
def get_all():
    data = json.loads(docker.get_all())
    return jsonify(data),200

# Get all running services
@app.route('/services/running')
def get_all_running():
    data = json.loads(docker.get_all())
    filtered_data = []

    for i in range(len(data)):
        if data[i]['State'] == 'running':
            filtered_data.append(data[i])

    return jsonify(filtered_data),200

# Get a specific service
# Get by ID
@app.route('/services/<id>')
def get_by_id(id):
    data = json.loads(docker.get_all())
    filtered_data = []

    for i in range(len(data)):
        print(data[i])
        if data[i]['ID'] == id:
            filtered_data.append(data[i])
    if not filtered_data:
        return jsonify({'error':'Invalid ID'}),404
    return jsonify(filtered_data),200

# Get by name
@app.route('/services/name/<name>')
def get_by_name(name):
    data = json.loads(docker.get_all())
    filtered_data = []
    print(data)
    for i in range(len(data)):
        print(data[i])
        if data[i]['Names'] == name:
            filtered_data.append(data[i])

    if not filtered_data:
        return jsonify({'error':'Invalid name'}),404

    return jsonify(filtered_data),200

# Create new services
@app.route("/services", 
methods = ['POST'])
def create_service():
    if not request.data:
        return jsonify({'error':'Bad Request'}),400
    try:
        data = json.loads(request.data)
    except JSONDecodeError:
        return jsonify({'error':'Bad request'}),400
    if 'image' not in data or not 'detached' in data or not 'publish' in data:
        return jsonify({'error':'Bad Request'}),400
    res = docker.create(data['image'],data['detached'],data['publish'])
    if res:
        print(res)
        return jsonify(res),400
    return jsonify({'body': 'Successfuly created'}),201

# Get latest service (optional - get latest by image)
@app.route("/services/latest",defaults ={'image':None})
@app.route("/services/latest/<image>")
def get_latest(image):
    res = docker.get_latest(image)
    if not res:
        return jsonify({'error':'Not found'}),404
    data = json.loads(docker.get_latest(image))
    return jsonify(data)
    
@app.route("/config")
def refresh_config():
    docker.ensure_services_alive()
    return jsonify({'status':'Vital services are up'}),200

@app.route("/config/reset")
def periodic_check():
    res=docker.remove_unwanted_services()
    if 'error' in res:
        return res,500
    return res,200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    