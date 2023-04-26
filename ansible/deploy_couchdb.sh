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
#!/bin/sh

# Define environmental variables
nodes=(172.26.132.54 172.26.135.122) #recommended to be same as server ip
masternode=${nodes[0]}
my_ip=$(hostname -I | awk '{print $1}')
is_master=0
if [ "$my_ip" = "$masternode" ]; then
  is_master=1
fi

user='admin'
pass='admin'
VERSION='3.0.0'
cookie='a192aeb9904e6590849337933b000c99'

# Get all Docker images
sudo docker pull couchdb:${VERSION}

# Stop and remove existing Docker container for the current node
if [ ! -z $(sudo docker ps --all --filter "name=couchdb${my_ip}" --quiet) ]; then
  sudo docker stop $(sudo docker ps --all --filter "name=couchdb${my_ip}" --quiet)
  sudo docker rm $(sudo docker ps --all --filter "name=couchdb${my_ip}" --quiet)
fi

# Create container for the current node, open ports for distributed cluster communication
sudo docker create \
  -p 9100:9100 \
  -p 4369:4369 \
  -p 5984:5984 \
  --name couchdb${my_ip} \
  --env COUCHDB_USER=${user} \
  --env COUCHDB_PASSWORD=${pass} \
  --env COUCHDB_SECRET=${cookie} \
  --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${my_ip}\"" \
  couchdb:${VERSION}

# Start and run Docker container for the current node
sudo docker start couchdb${my_ip}

if [ $is_master -eq 1 ]; then
  echo "This server is the master node."
else
  echo "This server is an other node."
fi
