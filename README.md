# COMP90024 Cluster and Cloud Computing Assignment 2

## Deploy Streamer Node (UK Server)

### Docker Command for Streamer UK

docker build -t streamer_uk --platform linux/amd64 .

docker tag streamer_uk luchen2001/mrc:streamer_uk 

docker push luchen2001/mrc:streamer_uk



