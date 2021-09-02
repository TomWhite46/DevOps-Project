# Emily's and Tom's DevOps Project

## 1 Creation of AWS structure

### VPC, Subnets and Security Groups Created
* VPC: a VPC with CIDR 10.0.0.0/16 was set up.
* Separate security groups for EC2 and RDS created:
  * EC2 instance security, allowing traffic from all sources on port 80 and 5000 (for the nginx and frontend containers) from dev IP on 22, and from within the VPC for other ports required by the app or by Docker.
  * Database security, allowing traffic only from within the VPC on port 3306.


### EC2 and RDS instances set up
* RDS mysql created and given database security group.
* 3 EC2 instances created: one for the manager of the swarm, two others to be workers. Only manager EC2 used until swarm set up (below).
![Imgur](https://i.imgur.com/bx43G85.png)


## 2 Microservice setup
### SSH into EC2 instance, install Docker and Docker-Compose
### Basic Services set up:
#### Materials for Docker containers for each microservice created:
* **Nginx**: nginx.conf file set up to run as reverse proxy, redirecting http traffic on port 80 to the EC2's IP address at port 5000, where the Flask app frontend is set to listen.  
![Imgur](https://i.imgur.com/GVg300D.png)
* **Flask App Frontend**

* **Flask App Backend**

#### Services set up:
* Database: ```Create.sql``` file run on RDS to create initial database and data.
* For frontend and backend, docker images created with ```docker build``` commands.
* Nginx, frontend and backend run with ```docker run``` commands. For nginx, the nginx.conf file was bind mounted to the container with the ```--mount``` option and port 80 was opened on the EC2 using ```-p 80:80```.

By running ```curl localhost``` on the EC2 instance and by navigating to the EC2's public IP address in a browser, the app was confirmed to be functional, as the data was retrieved from the database and returned in HTML format:
![Imgur](https://i.imgur.com/Er92THN.png)  
![Imgur](https://i.imgur.com/vtr7EGE.png) 

## 3 Docker-compose
A docker-compose.yaml could then be created, referring to the Dockerfiles created above for the build stage.
![Imgur](https://i.imgur.com/zDRTFEH.png)
At this stage, as not currently using Docker Swarm, container_name was set for the frontend and backend services.

## 4 Docker swarm stack
### Upload the images to Docker hub.
#### Make sure the build commands in the docker-compose.yaml refer to them.

## 5 Jenkins
### Pipeline created, associated with Github repo
![Imgur](https://i.imgur.com/e0Msn5M.png)

### Jenkinsfile on Github set up to run Docker on EC2:
![Imgur](https://i.imgur.com/m1Y70g6.png)

Note that credentials were set up as secrets in Jenkins in order to protect the database password.
![Imgur](https://i.imgur.com/SFHCDQ8.png)

### Webhook set up
![Imgur](https://i.imgur.com/lrgJKjm.png)

Commits to main on Github now caused automatic rebuild on Jenkins.

### Python testing with pytest
Python3 installed on EC2 instance, and script for python tests added to Jenkinsfile.
![Imgur](https://i.imgur.com/Xmo46RA.png)
