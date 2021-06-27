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
- [x] Add command line that will work once a day that will sync what existed in setting and dump it into the redis
- [x] add service that will get setting include casting from str to object (if it json) or to int, bool, float
- [x] sync process will work as follow: will have general flag in redis that flag params need go to old values the update will happen as follows  
        old value will save same key with the prefix env_[key]_temp  and new will override the env_[key] with new value once done reset flag in case of failure there need add flow for
        rollback that will fetch the  env_[key]_temp and return to the env_[key] as well reset flag

#### Upload files workflow logic overall
- [x] Upload files with relevant metadata
- [x] Check if folder exist (unless it root)
- [x] Check if entity_id existed (if type is user or store)
- [x] check if files validate (both size and type)
- [x] check permission if type=user (it his own user or support allow to upload files directly)
- [x] check permission if type=store (you within the group allow uploading) or/and you are the within staff/owner of the store or you support user allow to upload as well
- [x] check permission if type=system if you within staff platform
- [x] upload files to relevant location
- [x] register files on db
- [x] return db files register to client

#### Create Folder workflow logic overall
- [x] check if user have the correct permissions to do this action
- [x] check if sub path existed and register
- [x] create folder & create record
- [x] return record

#### List of Files/Folder
this will fetch list of files/ folder sort by name, size with paging support
#### Delete Folder workflow logic overall
- [x] check if user have the correct permissions to do this action
- [x] Locate all relevant file both on sub path and the dest folder
- [x] Locate all sup folders
- [x] Remove all db files records
- [x] Remove All Relevant files
- [x] Remove folder and sub folder records
- [x] remove the folders itself
##### Step I
- [x] check if user have the correct permissions to do this action
- [x] Locate all sup folders
- [x] Remove folder and sub folder records
- [x] remove the folders itself
##### Step II
- [x] this start after upload process will be done
- [x] Locate all relevant file both on sub path and the dest folder
- [x] Remove all db files records
- [x] Remove All Relevant files
### Tests
- [x] check on the model media get_all_parent_folders see if it give all relevant items create till lvl 4 items
- [x] DI Checks overall system check that all still work as intended
- [x] check task sync from settings
- [x] check get settings
- [x] check none existed settings
- [x] check force sync settings via service
#### Create Folder
- [x] check system folder create with incorrect permissions
- [x] check system folder create (root level)
- [x] check system folder create (sub folder level 1)
- [ ] check system folder create (sub folder level 2)
- [x] Check create root user folder
  - [x] check folder create with incorrect permissions
  - [x] check sup folder creation (level 1)
  - [ ] check sup folder creation (level 2)
- [x] Check create root store folder
  - [x] check folder create with incorrect permissions
  - [x] check sup folder creation ( level 1)
  - [ ] check sup folder creation ( level 2)
#### Delete Folders
- [ ] check folder delete with incorrect permissions
- [ ] delete folder root level on type user
  - [ ] check both db records and actual files has been deleted
- [ ] delete folder root level on type stores
  - [ ] check both db records and actual files has been deleted
- [ ] delete folder root level on type system
  - [ ] check both db records and actual files has been deleted

#### Upload Files
- [x] check files upload with incorrect permissions
- [x] upload files with correct metadata
- [x] check if files existed abd db records existed
- [x] upload files to sub path

#### Delete Files
- [ ] check folder delete with incorrect permissions
- [ ] delete files and check if files existed abd db records not existed
