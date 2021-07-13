from json.decoder import JSONDecodeError
from flask import Flask , request, jsonify
from services import docker_service
import json
from flask_apscheduler import APScheduler

app = Flask(__name__)

# Services health check logic
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
INTERVAL_TASK_ID = 'interval-task-id'

scheduler.add_job(
    id=INTERVAL_TASK_ID,
     func =docker_service.health_check,
      trigger='interval',
       seconds=10)

#Homepage
@app.route("/")
def homepage():
    return "Mini-Kubernetes!"

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
    res = docker_service.create(data['image'],data['detached'],data['publish'])
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
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    