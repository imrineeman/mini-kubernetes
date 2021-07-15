# Mini Kubernetes
### A simplified containerized services manager
The project consists of two services - `controller` and `scheduler`.</br>
* `controller` - controls all of the relevant micro-services specified in the configuration file (docker-compose.yml), and features a convinient API to fetch relevant data and operate on the system (e.g. run another service).
* `scheduler` - a service that sends HTTP request periodically to the `controller`, in order to invoke methods that ensure that the correct services are run on the system. </br>

To run the project - please build each image with with the specified command under it's relevant directory (if you wish to change the image's name, please change the environment variable accordingly). </br>
* Ensure python3-pip is installed `sudo apt-install python3-pip` </br>
* Run `docker build -t controller:latest ./services/controller` </br>
* Run `docker build -t scheduler:latest ./services/scheduler` </br>
* Create virtual environment </br>
* Run `pip3 install -r requirements.txt` </br>
* Run `python3 run.py` </br>

## API Documentation
*Show All Services*
----
  Returns JSON data about all services 

* **URL**

  `/services`

* **Method:**

  `GET`

* **Error Response:**

  * **Code:** `404` <br />
  * **Content:** `{'error':'Not found'}`
    
*Show Specific Service*
----
  Returns JSON data about a specific service (filter by ID or name).

* **URL**

  `/services/:id`
  
  
  `/services/name/:name`

* **Method:**

  `GET`
  
* **Success Response:**

  * **Code:** `200` <br />
  
* **Error Response:**
  * **Code:** `404` <br />
  * **Content:** `{'error':'Not found'}`
    
  * **Code:** `404` <br />
  * **Content:** `{'error':'Not found'}`


*Show Latest Service*
-----    
  Returns JSON data about the latest service that ran on the system (filter by image).

* **URL**

  `/services/latest`
  
  
  `/services/latest/:image`

* **Method:**

  `GET`
  
* **Success Response:**

  * **Code:** `200` <br />
 
* **Error Response:**
  * **Code:** `404` <br />
  * **Content:** `{'error':'Not found'}`
    
 *Create New Service*
 ----
 
   Create new service to run on the system

* **URL**

  `/services`
  
* **Method:**

  `POST`
  
* **Data Params**

  `image,String` - Image name. </br>
  `detached,Boolean` - Will the new service run as detached? (relevant for up to step 2) </br>
  `publish,Boolean\Int` - Publish the exposed port? (if `True` then publish random port, if `Int` published to the given port number). </br>
  
* **Success Response:**

  * **Code:** `201` <br />
  * **Content:** `{'body' : 'Successfuly created!'}`
 
* **Error Response:**
  * **Code:** `400` <br />
  * **Content:** `{ 'error' : 'Bad Request' }`

