# COMP90024 Cluster and Cloud Computing Assignment 2

## Deploy Streamer Node (UK Server)

### Docker Command for Streamer UK

docker build -t streamer_uk --platform linux/amd64 .

docker tag streamer_uk luchen2001/mrc:streamer_uk 

docker push luchen2001/mrc:streamer_uk

### Deploy the CouchDB and Streamer in Cloud

bash deploy_couchdb.sh

bash add_group.sh

docker run luchen2001/mrc:streamer_uk

## Deploy Server1/2

### Docker Command for Server

Docker build -t server1 --platform linux/amd64 .

Docker tag server1 luchen2001/mrc:server1

Docker push luchen2001/mrc:server1

### Deploy the CouchDB and Server in Cloud

bash deploy_couchdb.sh

bash add_group.sh

