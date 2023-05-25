# docker group

# Team 84 - Melbourne
# Brendan Pichler(bpichler@student.unimelb.edu.au) 1212335
# George Wang (wagw@student.unimelb.edu.au) 1084224
# Luchen Zhou(luczhou@student.unimelb.edu.au) 1053412
# Wei Wang(wangw16@student.unimelb.edu.au) 900889
# Yihan Wang (yihwang3@student.unimelb.edu.au) 1056614

groupadd docker
sudo gpasswd -a ubuntu docker
newgrp docker
sudo service docker restart
newgrp – docker
