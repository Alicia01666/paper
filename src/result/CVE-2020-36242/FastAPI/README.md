# 1. HOW TO RUN   
#### - Installations 
         - pip3 install -r requirements.txt

* Clone or download the github repository.
* Navigate to the project directory and start the server by typing “uvicorn main:app —reload”. 

# 2. GETTING STARTED

This project is a FastAPI application that does API key-based authentication and authorisation. 

The repository has five files - 

- **[crud.py]** - generates and stores the encryption key and inserts and fetches the user details.
- **[schemas.py]** - defines the pydantic models which acts as the base class for creating user defined models.
- **[sql_model.py]** - connects to the database and creates relations to store the user details.
- **[secret.key]** - stores the encryption key.
- **[main.py]** - the main FastAPI code that contains three endpoints-
    
    - **/register** : Capture the following fields:
    
     _User name_  - user input
    
    _Email_ – user input
    
    _Expiry date_ – should be 1 year from register date.
    
    _API_ – create a 10 digit alpha numeric API key for the user and store it encrypted in DB.
    
    - **/user/authenticate -** authenticates the user on login through swagger UI. The endpoint takes the API key as input on clicking the default Authorise button.
    - **/getUserData -** Authorises the user on accessing this url and returns user name and email address. Handles error scenarios with appropriate status codes like 400, 402 500 for – 1. User does not exits. 2. Invalid API key 3. Key expired.
