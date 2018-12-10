#### Todo REST API
This is a  **RESTFul API** developed in Flask With JSON Web Token Authentication and Flask-SQLAlchemy 
It is my very first REST API to develop. I have hopes of adding more functions. Feel free to make use of it.

#### Requirements
- [Python](https://www.python.org/) A general purpose programming language
- [Pip](https://pypi.org/project/pip/) A tool for installing python packages
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)  A tool to create isolated Python environments


#### Development setup
- Create a virtual environment and activate it
  ```bash
   virtualenv venv
   source /venv/bin/activate
  ```
- Install dependencies 
  ```bash
  pip install requirements.txt
  ```

#### Run the application
- In the terminal, run the following command so as to run the application
    ```bash
    python api.py
    ```

#### API REST End Points
- Simply simulate these endpoints using Postman. 

    | End Point                                           | Verb |Use                                            |
    | ----------------------------------------------------|------|-----------------------------------------------|
    |`/user`                                              |GET   |Gets a list of users and their details                                    |
    |`/user/<public_id>`                                  |GET   |Gets a specific user with the details                     |
    |`/user`                                              |POST  |Create a new user                   |
    |`/user/<public_id>`                                  |PUT   |Updates an existing user data         |
    |`/user/<public_id>`                                  |DELETE|Deletes a specific user                   |
    |`/todo`                                              |GET   |Gets a list of todos                    |
    |`/todo/<todo_id>`                                    |GET   |Gets details of a specific todo          |
    |`/todo/<todo_id>`                                    |POST  |Creates a todo                |
    |`/todo/<todo_id>`                                    |PUT   |Updates a todo to have been complete                         |
    |`/todo/<todo_id>`                                    |DELETE|Deletes a specific todo                     |
    

#### Built With
- [Flask](http://flask.pocoo.org/) A microframework for Python based on Werkzeug, Jinja 2 

#### Do more
- Go to [Jusutech](http://jusutech.blogspot.com) to get more details about this API