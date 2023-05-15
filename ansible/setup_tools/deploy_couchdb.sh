#!/bin/sh

# Update package lists and install dependencies
echo "Updating package lists and installing dependencies..."
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker repository and import its GPG key
echo "Adding Docker repository and importing GPG key..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package lists again and install Docker CE
echo "Installing Docker CE..."
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Add current user to the Docker group
echo "Adding current user to the Docker group..."
sudo usermod -aG docker $USER

# Enable and start Docker service
echo "Enabling and starting Docker service..."
sudo systemctl enable docker
sudo systemctl start docker

echo "Docker is now installed and ready to use."

# Define environmental variables
user='admin'
pass='admin'
VERSION='3.0.0'
cookie='a192aeb9904e6590849337933b000c99'

# Get Docker image
sudo docker pull couchdb:${VERSION}

# Stop and remove existing Docker container
if [ ! -z $(sudo docker ps --all --filter "name=couchdb" --quiet) ]; then
  sudo docker stop $(sudo docker ps --all --filter "name=couchdb" --quiet)
  sudo docker rm $(sudo docker ps --all --filter "name=couchdb" --quiet)
fi

# Create container and open ports for distributed cluster communication
sudo docker create \
  -p 9100:9100 \
  -p 4369:4369 \
  -p 5984:5984 \
  --name couchdb \
  --env COUCHDB_USER=${user} \
  --env COUCHDB_PASSWORD=${pass} \
  --env COUCHDB_SECRET=${cookie} \
  --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@$(hostname -I | awk '{print $1}')\"" \
  --volume /mnt/database:/opt/couchdb/data \
  couchdb:${VERSION}

# Start and run Docker container
sudo docker start couchdb

echo "CouchDB is now installed and ready to use."

# Create the directory, format the volume, and mount it
sudo mkdir /mnt/database
sudo mkfs.ext4 /dev/vdb
sudo mount /dev/vdb /mnt/database
echo "Created directory and mounted volume"
