# Tasks for user system
Task for the user system
## Tests
- [x] Add Test for route that mark tutrial as passed
- [x] Add Test for route that update user info as passed
- [x] Add Test for route that update user info as passed as support user
- [x] Add Test for route that update user info as passed as support user on different store

### Tests Staff Route

- [x] Add Test for route that add user staff by the owner as passed
- [x] Add Test for route that add user staff not by the owner as passed
- [x] Add Test for route that add user staff bt platform support
- [x] Add Test for route that add user staff by the owner of different store as not passed

### Tests get user queries Route


- [x] create logic for getting user by platform and store via filters [ filters: store_code,  emails , full name , country] and order by  [ create_at , full name , email,   stores ]
    - [x] Add Test For Get Platform User list With no filters
    - [x] Add Test For Get Platform User list With email filters
    - [x] Add Test For Get Platform User list With fullname filters
    - [x] Add Test For Get Platform User list With inactive filters
    - [x] Add Test For Get Platform User list With multi filters [ fullname, email]
    - [ ] Add Test For Get Platform User list With stores filters
    - [ ] Add Test For Get Platform User list With multi filters [ stores,fullname]
    - [ ] Add Test For Get Stores User list With no filters
    - [ ] Add Test For Get Stores User list With email filters
    - [ ] Add Test For Get Stores User list With fullname filters
    - [ ] Add Test For Get Stores User list With inactive filters
    - [ ] Add Test For Get Stores User list With multi filters [ fullname, stores]
    - [ ] Add Test For Get Stores User list With order by ->  no order provided
    - [ ] Add Test For Get Stores User list With order by ->  email order provided
    - [ ] Add Test For Get Stores User list With order by ->  fullname order provided
    - [ ] Add Test For Get Stores User list With order by ->  store order provided
    - [ ] Add Test For Get Stores User list With order by ->  create_at order provided
    - [ ] Add Test For Get Platform User list With multi order by ->  store,email order provided
    - [ ] Add Test For Get Stores User list With unknown column  order by-> get 400 (invalid params)
    - [ ] Add Test For Get Stores User list paginate (test 3 pages)
  - [ ] User test Permissions for Get List of Users
    - [ ] Add Test For Get Platform User list  , Role Platform user  , platform Filters , no order by
    - [ ] Add Test For Get Platform User list  , Role Store Staff user -> show error   , platform Filters , no order by
    - [ ] Add Test For Get Stores User list  , Role Platform user    , stores Filters , no order by
    - [ ] Add Test For Get Stores User list With store staff user  , stores Filters , no order by


