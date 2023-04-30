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

docker run -p 8000:8000 luchen2001/mrc:server1

### set up CouchDB cluster

bash set_cluster.sh

## Deploy the Frontend Server

### Dockerize the React app & Nginx load balancer

docker build -t frontend --platform linux/amd64 .

docker tag frontend luchen2001/mrc:frontend

docker push luchen2001/mrc:frontend

docker build -t loadbalancer --platform linux/amd64 .

docker tag loadbalancer luchen2001/mrc:loadbalancer

docker push luchen2001/mrc:loadbalancer

### set up the frontend server

bash set_docker.sh

bash add_group.sh 

- Copy the docker-compose.yml

docker compose up -d
