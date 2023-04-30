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