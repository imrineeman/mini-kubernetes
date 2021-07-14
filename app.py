from flask import Flask , request, jsonify
from services import docker

app = Flask(__name__)

#Homepage
@app.route("/")
def homepage():
    return "Mini-Kubernetes!"

# Get all services
@app.route('/services')
def get_all():
    data = docker.get_all()
    if 'error' in data:
        return jsonify(data),500
    return jsonify(data),200

# Get all running services
@app.route('/services/running')
def get_all_running():
    data = docker.get_all()
    if 'error' in data:
        return jsonify(data),500

    filtered_data = []

    for i in range(len(data)):
        if data[i]['State'] == 'running':
            filtered_data.append(data[i])

    return jsonify(filtered_data),200

# Get a specific service
# Get by ID
@app.route('/services/<id>')
def get_by_id(id):
    data = docker.get_all()
    if 'error' in data:
        return jsonify(data),500
       
    filtered_data = []
    for i in range(len(data)):
        if data[i]['ID'] == id:
            filtered_data.append(data[i])

    if not filtered_data:
        return jsonify({'error':'Invalid ID'}),404
    return jsonify(filtered_data),200

# Get by name
@app.route('/services/name/<name>')
def get_by_name(name):
    data = docker.get_all()
    if 'error' in data:
        return jsonify(data),500
    filtered_data = []
    for i in range(len(data)):
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
    
    data = docker.get_all()
    if 'error' in data:
        return jsonify(data),500
       
    if 'image' not in data or not 'detached' in data or not 'publish' in data:
        return jsonify({'error':'Bad Request'}),400
    res = docker.create(data['image'],data['detached'],data['publish'])
    
    if res:
        return jsonify(res),400
    return jsonify(res),201

# Get latest service (optional - get latest by image)
@app.route("/services/latest",defaults ={'image':None})
@app.route("/services/latest/<image>")
def get_latest(image):
    res = docker.get_latest(image)
    if 'error' in res:
        return jsonify({'error':'Not found'}),404
    return jsonify(res),200

# Endpoint for scheduler service - 
@app.route("/config")
def refresh_config():
    res = docker.ensure_services_alive()
    return jsonify(res),200

# Endpoint for scheduler service
@app.route("/config/reset")
def periodic_check():
    res=docker.remove_unwanted_services()
    if 'error' in res:
        return res,500
    return res,200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    