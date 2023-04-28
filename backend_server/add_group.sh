# docker group
groupadd docker
sudo gpasswd -a ubuntu docker
newgrp docker
sudo service docker restart
newgrp – docker
