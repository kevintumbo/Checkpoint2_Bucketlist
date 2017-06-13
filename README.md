# CP2--BucketList-Application-API
[![Build Status](https://travis-ci.org/kevintumbo/Checkpoint2_Bucketlist.svg?branch=tests)](https://travis-ci.org/kevintumbo/Checkpoint2_Bucketlist)
[![Coverage Status](https://coveralls.io/repos/github/kevintumbo/Checkpoint2_Bucketlist/badge.svg?branch=tests)](https://coveralls.io/github/kevintumbo/Checkpoint2_Bucketlist?branch=tests)

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
clone the repository.
cd into the repo and checkout to the master branch.
Create an isolated virtual environment.
Install the dependencies via pip install -r requirements.txt.
create a .env file and add the following.

```sh
source name-of-virtual-environment/bin/activate
export FLASK_APP="run.py"
export SECRET="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
export APP_SETTINGS="development"
```

### Setup Up Database And Migrations
run migrations.
*python manage.py db init
*python manage.py db migrate
*python manage.py db upgrade
*Flask Run

when you run the server it should print out
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

### 

to run tests run

*nosetests --with-coverage --cover-package=bucketlist

This will return the number of tests run and the coverage of the tests.

## How To Use Bucketlist Api(example)

### Register A User

-POST : http://127.0.0.1:5000/api/v1.0/auth/register

-Body : {"username":"John", "email":"john@gmail.com", "password":"password"}

![Alt text](https://image.ibb.co/j2W57a/Screen_Shot_2017_06_12_at_14_39_29.png "create user")

-POST : http://127.0.0.1:5000/api/v1.0/auth/login

-Body : {"email": "john@gmail.com", "password": "password"}

![Alt text](https://image.ibb.co/kHNpYF/Screen_Shot_2017_06_12_at_14_39_42.png "Log in user")

### Create a Bucketlist

-POST : http://127.0.0.1:5000/api/v1.0/bucketlists/

-Body : {"name":"Hobbies", "description":"My hobbies"}

![Alt text](https://image.ibb.co/f6d7Lv/Screen_Shot_2017_06_12_at_14_40_15.png "create Bucketlist")

### Return a Bucketlist using id

-GET : http://127.0.0.1:5000/api/v1.0/bucketlists/1

![Alt text](https://image.ibb.co/dG9gfv/Screen_Shot_2017_06_12_at_14_40_35.png "Return Bucketlist")

### Return a Bucketlist using name

-GET : http://127.0.0.1:5000/api/v1.0/bucketlists?q=hobbies

![Alt text](https://image.ibb.co/c3407a/Screen_Shot_2017_06_12_at_15_25_46.png "Return Bucketlist using name")

### Update A bucketlist

-PUT : http://127.0.0.1:5000/api/v1.0/bucketlists/1

-Body : {"name":"Updated Hobbies", "description":" Updated My hobbies"}

![Alt text](https://image.ibb.co/foywDF/Screen_Shot_2017_06_12_at_14_41_09.png "Update Bucketlist")

### Create an item in the bucketlists

-POST : http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/

-Body : {"item_name":"cycling", "item_description":"Go cycling"}

![Alt text](https://image.ibb.co/kZQySa/Screen_Shot_2017_06_12_at_14_41_49.png "Create Bucketlist item")

### Retrive A BucketList Item using id

-GET : http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/1

![Alt text](https://image.ibb.co/kfdwDF/Screen_Shot_2017_06_12_at_14_42_15.png "Return Bucketlist Item")

### Update A BucketList Item

-PUT : http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/1

-Body : {"item_name":"update cycling", "item_description":" update Go cycling"}

![Alt text](https://image.ibb.co/foywDF/Screen_Shot_2017_06_12_at_14_41_09.png "Update Bucketlist Item")

### Delete a bucketlist item

-DELETE : http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/1

![Alt text](https://image.ibb.co/iUegfv/Screen_Shot_2017_06_12_at_14_43_24.png "Delete Bucketlist item")

### Delete A bucketlist

-DELETE : http://127.0.0.1:5000/api/v1.0/bucketlists/1

![Alt text](https://image.ibb.co/buSsLv/Screen_Shot_2017_06_12_at_15_15_28.png "Delete Bucketlist")

Author
----
	-Kevin Tumbo


