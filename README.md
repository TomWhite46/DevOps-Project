# QAC SFIA2 Project

This application is a simple [Flask application](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application), ready to be deployed, for your SFIA2 project.

The following information should be everything you need to complete the project.

## Brief

The application must:

- Be tested 
- Be deployed to a **Virtual Machine**
- Make use of a **managed Database solution**

## Application

The application is a Flask application running in **2 micro-services** (*frontend* and *backend*).  

The database directory is available should you: 
  - want to use a MySQL container for your database at any point, *or*
  - want to make use of the `Create.sql` file to **set up and pre-populate your database**.

The application works by:
1. The frontend service making a GET request to the backend service. 
2. The backend service using a database connection to query the database and return a result.
3. The frontend service serving up a simple HTML (`index.html`) to display the result.

### Database Connection

The database connection is handled in the `./backend/application/__init__.py` file.

A typical Database URI follows the form:

```
mysql+pymysql://[db-user]:[db-password]@[db-host]/[db-name]
```

An example of this would be:

```
mysql+pymysql://root:password@mysql.123456.rds.amazonaws.com:3306/orders
```

### Environment Variables

The application makes use of **2 environment variables**:

- `DATABASE_URI`: as described above
- `SECRET_KEY`: any *random string* will work here

### Running a Flask Application

Typically, to run a Flask application, you would:

1. Install the pip dependencies from a `requirements.txt`, these can be found in the `backend` and `frontend` directories:

```
pip3 install -r requirements.txt
```

2. Run the application:

```
python3 app.py
```

![app-diagram](https://i.imgur.com/wnbDazy.png)

## Testing

Unit Tests have been included for both the frontend and backend services.


You can run the tests using the command:

```
python3 -m pytest
```

To generate a coverage report, you will need to run:

```
python3 -m pytest --cov application
```

## Infrastructure

The **Minimum Viable Product** for this project should at least demonstrate the following infrastructure diagram:

![mvp-diagram](https://i.gyazo.com/f5cd176c4f440af639b7dc3c098535c7.png)

**Good luck!**
