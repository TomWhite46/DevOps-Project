# Emily's and Tom's DevOps Project

# Contents
1. Jira Board
2. Risk Assessment
3. Creation of AWS structure
4. Microservice setup
5. Docker Compose
6. Docker Swarm Stack
7. Jenkins
8. Python testing
<br><br>

# 1 Jira Board
The Jira board can be found [here](https://bootcampbae.atlassian.net/jira/software/projects/DEV/boards/6).
Jira stories were created and assigned to 6 overarching epics for different aspects of the project; every story was given a priority assessment and a story point estimate.  
![Imgur](https://i.imgur.com/DxYqZDF.png)
The stories were then put into a sprint to last the duration of the project. Items were moved across the sprint's Kanban board in real time, as we completed the tasks.  
![Imgur](https://i.imgur.com/jANge5c.png)

# 2 Risk Assessment

# 3 Creation of AWS structure

## VPC, Subnets and Security Groups Created
* VPC: a VPC with CIDR 10.0.0.0/16 was set up.
* Separate security groups for EC2 and RDS created:
  * EC2 instance security, allowing traffic from all sources on port 80 and 5000 (for the nginx and frontend containers) from dev IP on 22, and from within the VPC for other ports required by the app or by Docker.
  ![Imgur](https://i.imgur.com/Eou6u56.png)
  * Database security, allowing traffic only from within the VPC on port 3306.
  ![Imgur](https://i.imgur.com/gLB7NMn.png)


## EC2 and RDS instances set up
* RDS mysql created and given database security group.
* 3 EC2 instances created: one for the manager of the swarm, two others to be workers. Only manager EC2 used until swarm set up (below).
![Imgur](https://i.imgur.com/bx43G85.png)


# 4 Microservice setup
## SSH into EC2 instance, install Docker and Docker-Compose
## Basic Services set up:
### Materials for Docker containers for each microservice created:
* **Nginx**: nginx.conf file set up to run as reverse proxy, redirecting http traffic on port 80 to the EC2's IP address at port 5000, where the Flask app frontend is set to listen.  
![Imgur](https://i.imgur.com/GVg300D.png)
* **Flask App Frontend**  
The frontend app required python and the files specified in the requirements.txt file; investigation of app.py showed that it needed port 5000 exposed.  
![Imgur](https://i.imgur.com/G3R3ITn.png)

* **Flask App Backend**
Similarly, the backend app required python and the files specified in the requirements.txt file; investigation of app.py showed that it needed port 5001 exposed.  
![Imgur](https://i.imgur.com/U9O9xih.png)

### Services set up:
* Database: ```Create.sql``` file run on RDS to create initial database and data.
* For frontend and backend, docker images created with ```docker build``` commands.
* Nginx, frontend and backend run with ```docker run``` commands. For nginx, the nginx.conf file was bind mounted to the container with the ```--mount``` option and port 80 was opened on the EC2 using ```-p 80:80```.

By running ```curl localhost``` on the EC2 instance and by navigating to the EC2's public IP address in a browser, the app was confirmed to be functional, as the data was retrieved from the database and returned in HTML format:
![Imgur](https://i.imgur.com/Er92THN.png)  
![Imgur](https://i.imgur.com/vtr7EGE.png) 

# 5 Docker-compose
A docker-compose.yaml could then be created, referring to the Dockerfiles created above for the build stage.  
![Imgur](https://i.imgur.com/zDRTFEH.png)  
At this stage, as not currently using Docker Swarm, container_name was set for the frontend and backend services.

# 6 Docker swarm stack
## Swarm created
Swarm created on the manager EC2 using the command ```docker swarm init```; the other two EC2s were connected to the sawrm using the token provided.  
![Imgur](https://i.imgur.com/Jlc5NOB.png)

## Upload the images to Docker hub
Custom Docker images for the frontend and backend were pushed to DockerHub, so that they can be accessed from any EC2 instance.  
![Imgur](https://i.imgur.com/lAlryI2.png)

## docker-compose.yaml edited
Then the docker-compose.yaml was edited to ensure that the images specified were those on Docker. The number of replicas for the swarm stack to build was also specified.  
![Imgur](https://i.imgur.com/msVaQeB.png)  

## Stack 
The stack was then deployed using ```docker stack deploy --compose-file docker-compose.yaml project-stack```. Containers were then deployed across the three EC2 instances in the swarm: 
![Imgur](https://i.imgur.com/FpwFFpb.png)

# 7 Jenkins
## Pipeline created, associated with Github repo
![Imgur](https://i.imgur.com/e0Msn5M.png)

## Jenkinsfile on Github set up to run Docker on EC2:
The deployment stage runs docker stack as had previously been done directly on the EC2 instance.  
![Imgur](https://i.imgur.com/m1Y70g6.png)

Note that credentials were set up as secrets in Jenkins in order to protect the database password.
![Imgur](https://i.imgur.com/SFHCDQ8.png)

## Webhook set up
![Imgur](https://i.imgur.com/lrgJKjm.png)

Commits to main on Github now caused automatic rebuild on Jenkins.

# 8 Python testing with pytest
Python3 installed on EC2 instance, and script for python tests added to Jenkinsfile.
![Imgur](https://i.imgur.com/Xmo46RA.png)  
On committing the updated Jenkinsfile to Github, the tests were run as part of the automatically triggered Jenkins build, showing a successful result.  
![Imgur](https://i.imgur.com/OWwRV4x.png)

