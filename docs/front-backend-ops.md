# Server Mapping
this server that later date will be split into microservices have many parts that required the client connections  as well later data BI and stats system that
will be required.

as well there a not want expose this server to outside and will require operations that are heavy both cpu or/and memory.

for that reason there going be will split to two main services

1. Backend service that will hold all data layer will be based PSQL later will base bigdata , it's have few Target logic:
   - Basic Ops - handle users (register user platform / site , customers of the site will not be registered from here will send only relevant data about it  based actions)
   - management assets (not view or download this need move) and upload will change to
     - Front backend will upload to temp
     - Front backend Request from Backend register on the asset
     - Backend do it thing and return media
   - create or control shops (only here able to create such a thing)
     - activity within the shop
     - transactions within shop
     - payments
   - dev ops operations
     - sync data with mongo where required
       - Users
       - Assets
       - Shops
         - Payments
         - transactions (shallow info)
         - Reports
   - Tasks

Side note check out this [link](https://www.frederikbanke.com/integration-testing-in-python-rabbitmq/) it about rabbitmq and python unit test see if helpful
max will setup a dev server just for the tests

2. Front Backend service this will control all aspect of user life as well request from backend make reports
   - All user operations
   - Request Offline Tasks
   - Control and Management Content (Pages and more)
   - Request operations that need backend
