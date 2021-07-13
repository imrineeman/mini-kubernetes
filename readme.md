# Mini Kubernetes!
Repository for Zadara's home assignment

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
  * **Content:** `{ error : "User doesn't exist" }`
    
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
  * **Content:** `{ error : "Invalid ID" }`
    
  * **Code:** `404` <br />
  * **Content:** `{ error : "Invalid Name" }`


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
  * **Content:** `{ error : "Invalid ID" }`
    
 *Create New Service*
 ----
 
   Create new service to run on the system

* **URL**

  `/services`
  
* **Method:**

  `POST`
  
* **Data Params**

  `image,String` - Image name. </br>
  `detached,Boolean` - Will the new service run as detached? </br>
  `publish,Boolean\Int` - Publish the exposed port? (if `True` then publish random port, if `Int` published to the given port number). </br>
  
* **Success Response:**

  * **Code:** `201` <br />
  * **Content:** `{'body' : 'Successfuly created!'}`
 
* **Error Response:**
  * **Code:** `400` <br />
  * **Content:** `{ error : "Bad Request" }`

