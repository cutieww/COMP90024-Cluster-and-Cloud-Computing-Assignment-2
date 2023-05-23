# COMP90024 Cluster and Cloud Computing Assignment 2 
#            Group 84


## Frontend website
http://172.26.131.144:3000/

## Youtube Video
System Deployment (scaling): https://www.youtube.com/watch?v=yRJuwNy1_7A&feature=youtu.be

Frontend Visualization: [https://www.youtube.com/watch?v=SoCIkHjk2eQ&t=51s](https://www.youtube.com/watch?v=dCwyQDXtk80)

## Architecture
<img width="828" alt="Screenshot 2023-05-17 at 12 12 40 am" src="https://github.com/cutieww/COMP90024-Cluster-and-Cloud-Computing-Assignment-2/assets/88120882/428d772d-51da-4916-ad5b-503ae2e5cd1e">


## Deployment Guide

### Deploy Streamer Node (World Server)

#### 1. Docker Command for Streamer World
```
$ docker build -t streamer_world --platform linux/amd64 .

$ docker tag streamer_world luchen2001/mrc:streamer_world

$ docker push luchen2001/mrc:streamer_world
```


####  2. Deploy the CouchDB and Streamer in Cloud
```
$ bash deploy_couchdb.sh

$ bash add_group.sh

$ docker run luchen2001/mrc:streamer_world
```
### Deploy Server1/2

#### 1. Docker Command for Server
```
$ Docker build -t server1 --platform linux/amd64 .

$ Docker tag server1 luchen2001/mrc:server1

$ Docker push luchen2001/mrc:server1
```
```
$ Docker build -t server2 --platform linux/amd64 .

$ Docker tag server2 luchen2001/mrc:server2

$ Docker push luchen2001/mrc:server2
```

#### 2. Deploy the CouchDB and Server in Cloud
```
$ bash deploy_couchdb.sh

$ bash add_group.sh

$ docker run -p 8000:8000 luchen2001/mrc:server1
```

#### 3. set up CouchDB cluster
```
$ bash set_cluster.sh
```
### Deploy the Frontend Server

#### 1. Dockerize the React app & Nginx load balancer
```
$ docker build -t frontend --platform linux/amd64 .

$ docker tag frontend luchen2001/mrc:frontend

$ docker push luchen2001/mrc:frontend

$ docker build -t loadbalancer --platform linux/amd64 .

$ docker tag loadbalancer luchen2001/mrc:loadbalancer

$ docker push luchen2001/mrc:loadbalancer
```
#### 2. set up the frontend server
```
$ bash set_docker.sh

$ bash add_group.sh 

# Copy the docker-compose.yml

$ docker compose up -d
```

### Stream Mastodon Server
Partly copy from COMP90024 gitlab in ado folder
#### 1. Installation

* Register on a Mastodon server of your choice and add an Application (this action generates an API Key that can be used to access that Masotdon server).

```shell
export MASTODON_ACCESS_TOKEN="<access token>>"
```
* Go to [Mastodon.py installation page](https://pypi.org/project/Mastodon.py/#files) and download the WHL file version `1.8.x`;
* Go to the folder by `cd harvester_node/streamer`
* Unzip the downloaded WHL file into current directory.
```shell
unzip file.whl
```

#### 2. for MacOS create the environment
create the virtual environment using `venv`. (Ensure the `venv` is installed).

```
$ python3 -m venv myvenvname
$ myvenvname CCC/bin/activate

# Ensure you are in the harvester_node/streamer directory
$ python -m pip install -r requirements.txt
$ pip3 install Mastodon.py
```


#### 3. stream the Mastodon server data into CouchDB
The access token has been hard code inside the [main.py](harvester_node/streamer/main.py).
```commandline
python main.py
```
 would stream the mastodon data we need into our couchDB with database named mastodon_policy.




### For Map Reduce
The map and reduce function in javascript are placed in the [map_reduce](map_reduce/) folder. 

With [mostodon_policy](map_reduce/mastodon_policy/) for the map and reduce function for mastodon server, while [twitter](map_reduce/twitter/) for the twitter data. 

For later streaming issue for mastodon server, we have change the format in python, written inside  [mastodon_process.py](backend_server/backend/mastodon_process.py).
#### 1. run inside the [map_reduce](map_reduce/) folder

Move the [Gruntfile.js](map_reduce/Gruntfile.js), [package.json](map_reduce/package.json), [package-lock.json](map_reduce/package-lock.json) from the classroom gitlab.


```
$ cd map_reduce

# the next 2 lines only run once
$ npm install
$ sudo npm install -g grunt-cli


$ bash reduce.sh
```

#### 2. run inside the [backend](backend_server/backend/) folder
```
# ensure enter the folder
$ cd backend_server/backend

# create virtual environment same in the stream Mastodon Server
$ python3 -m venv myvenvname
$ myvenvname myvenvname/bin/activate

# install the packages
$ python -m pip install -r requirements.txt

$ python mastodon_process.py
```
It would automatically update the mapreduce function in the couchDB mastodon database and get the result value into the backend.
