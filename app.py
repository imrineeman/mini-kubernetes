from flask import Flask , request, jsonify
from services import docker_service
import json
app = Flask(__name__)

# Create new service
@app.route("/services", 
methods = ['POST'])
def create_service():
    if not request.data:
        return jsonify({'error':'Bad Request'}),400
    data = json.loads(request.data)

    if 'image' not in data:
        return jsonify({'error':'Bad Request'}),400
    
    res = docker_service.create(data['image'])
    if res:
        print(res)
        return jsonify(res),400
    return jsonify({'status': 'Successfuly created'}),201

# Get latest service (optional - get latest by image)
@app.route("/services/latest",defaults ={'image':None})
@app.route("/services/latest/<image>")
def get_latest(image):
    res = docker_service.get_latest(image)

    if not res:
        return jsonify({'error':'Not found'}),404
        
    data = json.loads(docker_service.get_latest(image))
    return jsonify(data)
    