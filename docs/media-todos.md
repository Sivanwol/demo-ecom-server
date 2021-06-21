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

### Tasks
- [ ] Add command line that will work once a day that will sync what existed in setting and dump it into the redis
- [x] add service that will get setting include casting from str to object (if it json) or to int, bool, float
- [x] sync process will work as follow: will have general flag in redis that flag params need go to old values the update will happen as follows  
        old value will save same key with the prefix env_[key]_temp  and new will override the env_[key] with new value once done reset flag in case of failure there need add flow for
        rollback that will fetch the  env_[key]_temp and return to the env_[key] as well reset flag

### Tests
- [x] DI Checks overall system check that all still work as intended
- [ ] check task sync from settings
- [ ] check get settings
- [ ] check none existed settings
- [ ] check force sync settings via service
- [ ] Check create root user folder
  - [ ] check sup folder creation
- [ ] Check create root store folder
  - [ ] check sup folder creation
- [ ] Check create root system folder
  - [ ] check sup folder creation
