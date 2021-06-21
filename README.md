# Demo Shop Ecom

this will the operation of the Ecom shop that with user base of firebase

### Virtual environments

```angular2html
$ sudo apt-get install python-virtualenv
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install Flask

Install all project dependencies using:

```
When need install the deps of the system
```angular2html
$ pip install -r requirements.txt
```

if ever need add a dep to the project please do as follow
```angular2html
$ pip install packagename
$ pip freeze > requirements.txt # this will regenerate the requirements.txt
```

### Testing
see: [here](https://docs.python.org/3/library/unittest.htm)
<p>
for run use this command:
</p>

```angular2html
$ python -m unittest
```
### Running
 
```angular2html
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ python -m flask run
```

This launches a very simple builtin server, which is good enough for testing but probably not what you want to use in production.

If you enable debug support the server will reload itself on code changes, and it will also provide you with a helpful debugger if things go wrong.

If you have the debugger disabled or trust the users on your network, you can make the server publicly available simply by adding --host=0.0.0.0 to the command line:

```angular2html
$ flask run --host=0.0.0.0
```

### Developing and Testing
<p>
as this system have a firebase user system that it is based upon there is a need quick way</p>
<ul>
    <li>Getting Id token from n user that use the emulator (else just use the client for fetching the id token)</li>
    <li>Createing on new env master user that have role owner and able to do most stuff within system</li>
</ul>
as such there is two commands that able use both globally and within emulators
for change where the system will work need run this command:
<p><b>Note if any of the setup will set need make sure unset if want use globally</b></p>

###### Set up the auth system

```angular2html
# mac / linux
$ export FIREBASE_AUTH_EMULATOR_HOST=localhost:9099
# windows
$ set FIREBASE_AUTH_EMULATOR_HOST=localhost:9099
```
###### Set up the firestore system

```angular2html
# mac / linux
$ export FIRESTORE_EMULATOR_HOST=localhost:9099
# windows
$ set FIRESTORE_EMULATOR_HOST=localhost:9099
```

##### Command Lines

###### getting list of route on the system
```angular2html
$ python manage.py list_routes
```

###### sync the system settings table with redis (able do so in cli)
```angular2html
$ python manage.py sync_system
```

###### generate init settings for the system to operate
```angular2html
$ python manage.py init_system
```

###### set up of master account on Role of owner
```angular2html
$ python manage.py setup_owner email@domain.com password
```

###### set up of master account on Role of accounts
```angular2html
$ python manage.py setup_accounts email@domain.com password
```

###### set up of master account on Role of support
```angular2html
$ python manage.py setup_support email@domain.com password
```
###### getting id token from an account
```angular2html
$ python manage.py get_id_token email@domain.com password
```


### Running using Manager

This app can be started using Flask Manager. It provides some useful commands and configurations, also, it can be customized with more functionalities.

```angular2html
$ python manage.py runserver
```

### Alembic Migrations

Use the following commands to create a new migration file and update the database with the last migrations version:

```angular2html
$ flask db revision --autogenerate -m "description here"
$ flask db upgrade head
```

This project also uses the customized manager command to perform migrations.
```angular2html
$ python manage.py db revision --autogenerate -m "description here"
$ python manage.py db upgrade head
```

To upgrade the database with the newest migrations version, use:

```angular2html
$ python manage.py db upgrade head
```

### Task Controls

as any system there is a need for task control system for this the system use a Google functions and Cloud Tasks
