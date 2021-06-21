# Tasks for user system
Task for the media system

### File Upload Work flow

the file upload work flow is work as follows:

#### Workflow

- First Upload will happend locally
- The local server will compress and handle the file base it file profile
  - image (add them to que just create small preview for show the user something) - worth checkout and use https://imagekit.io/plans
    - pre resizing files
    - send them to the store folder / user folder
    - zip them and perp preview files
    - register on the db about the files and current status
  - video (add them to que just create small preview for show the user something)
    - compress and create screen shop (this subject to change as not sure how much i want handle be here i may end up use 3rd party)
    - send them to the store folder / user folder
    - zip them and perp preview files
    - register on the db about the files and current status
  - document / excel / pdf
    - send them to the store folder / user folder
    - zip them and perp preview files
    - register on the db about the files and current status
- upon the upload complete the files will register, and the client will get a progress id with the preview files if existed
- the client will see the progess id and will add internal checking when it's done (will send via web socket)
- files will be prep based the type
- files will register on db
- notify client and in general via websockets


### R&D

Solution I pick mostly for cost reason is monolith server mostly stuff will build on top of the system and not use the cloud as for cost (have almost zero ability to pay atm)

- [x] install web socket
- [x] install signals - not required and not useful
- [x] unit test for socket io -> https://github.com/miguelgrinberg/flack/blob/master/tests/tests.py

### Tests
- [ ] DI Checks overall system check that all still work as intended
- [ ] Check create root user folder
  - [ ] check sup folder creation
- [ ] Check create root store folder
  - [ ] check sup folder creation
- [ ] Check create root system folder
  - [ ] check sup folder creation
