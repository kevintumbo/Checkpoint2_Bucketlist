# CP2--BucketList-Application-API
[![Build Status](https://travis-ci.org/kevintumbo/Checkpoint2_Bucketlist.svg?branch=tests)](https://travis-ci.org/kevintumbo/Checkpoint2_Bucketlist)
[[![Coverage Status](https://coveralls.io/repos/github/kevintumbo/Checkpoint2_Bucketlist/badge.svg?branch=master)](https://coveralls.io/github/kevintumbo/Checkpoint2_Bucketlist?branch=tests)

### Bucketlist API

According to Merriam-Webster Dictionary, a Bucket List is a list of things that one has not done before but wants to do before dying.

This is an API for an online Bucket List service using Flask.

### Endpoints

Bucketlist Api has the following endpionts

| Endpoint | Functionality |
| -------- | ------------- |
| POST /auth/login | Logs a user in |
| POST /auth/register | Register a user |
| POST /bucketlists/ | Create a new bucket list |
| GET /bucketlists/	| List all the created bucket lists |
| GET /bucketlists/<id> | Get single bucket list |
| PUT /bucketlists/<id> | Update this bucket list |
| DELETE /bucketlists/<id> | Delete this single bucket list |
| GET /bucketlists/<id>/items/<item_id> | Get a single bucket list item |
| POST /bucketlists/<id>/items/ | Create a new item in bucket list |
| PUT /bucketlists/<id>/items/<item_id> | Update a bucket list item |
| DELETE /bucketlists/<id>/items/<item_id> | Delete an item in a bucket list |


### Installation
clone the repository
cd into the repo and checkout to the tests branch
Create an isolated virtual environment
Install the dependencies via pip install -r requirements.txt
create a .env file and add the following

```sh
source name-of-virtual-environment/bin/activate
export FLASK_APP="run.py"
export SECRET="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
export APP_SETTINGS="development"
```

### Setup Up Database And Migrations
run migrations
*python manage.py db init
*python manage.py db migrate
*python manage.py db upgrade
*Flask Run

when you run the server it should print out
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

### Testing
to run tests run

*nosetests --with-coverage --cover-package=bucketlist

This will return the number of tests run and the coverage of the tests.

## How To Use Bucketlist Api(example)

### Register A User
POST : http://127.0.0.1:5000/api/v1.0/auth/register
Body : {"username":"John", "email":"john@gmail.com", "password":"password"}

### Log in a user
POST : http://127.0.0.1:5000/api/v1.0/auth/login
Body : {"email": "john@gmail.com", "password": "password"}

### Create a Bucketlist
POST : http://127.0.0.1:5000/api/v1.0/bucketlists/
Body : {"name":"Hobbies", "description":"My hobbies"}

### Return a Bucketlist
GET : http://127.0.0.1:5000/api/v1.0/bucketlists/1

### Update A bucketlist
PUT : http://127.0.0.1:5000/api/v1.0/bucketlists/1
Body : {"name":"Updated Hobbies", "description":" Updated My hobbies"}


### Delete A bucketlist
DELETE : http://127.0.0.1:5000/api/v1.0/bucketlists/1

### Create an item in the bucketlists
POST : http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/
Body : {"item_name":"cycling", "item_description":"Go cycling"}

### Retrive A BucketList Item
GET : http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/1

### Update A BucketList Item
PUT : http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/1
Body : {"item_name":"update cycling", "item_description":" update Go cycling"}

### Delete a bucketlist item
DELETE : http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/1




