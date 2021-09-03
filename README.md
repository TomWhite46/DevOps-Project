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
9. Final test: update to python app
10. Stretch goal: deployment to separate dev site from dev branch
11. Further goals
12. Acknowledgements
<br><br>

# 1 Jira Board
The Jira board can be found [here](https://bootcampbae.atlassian.net/jira/software/projects/DEV/boards/6).
Jira stories were created and assigned to 6 overarching epics for different aspects of the project; every story was given a priority assessment and a story point estimate.  
![Imgur](https://i.imgur.com/DxYqZDF.png)
The stories were then put into a sprint to last the duration of the project. Items were moved across the sprint's Kanban board in real time, as we completed the tasks.  
![Imgur](https://i.imgur.com/jANge5c.png)
<br><br>

# 2 Risk Assessment  
## Initial assessment
An initial risk assessment was drawn up, including general risks relating to working environment and specific risks relating to the network infrastructure that was to be created.  
Each item was given an estimation of likelihood and impact, from which an overall risk assessment rating was creating, using a likelihood-impact matrix.  
For each item, measures were determined to reduce the risk and/or the impact wherever possible.
![Imgur](https://i.imgur.com/kRXnP4V.png)  
<br>

## Risk reviews  
At two points during the project, a review of the risk factors was conducted, during which the risk assessment of existing items was reconsidered, and new items added to reflect new risks that had arisen.  
For pre-existing risks, the assessment tended downwards over time, as increasing completion of the project reduced the potential impact of any issues that affected our ability to meet the final deadline.

### Review 1  
After the creation of the AWS network, most of the risks remained the same, but the new risk of the main EC2 instance failing while it contained the ongoing work was added.
![Imgur](https://i.imgur.com/1pJlzlL.png)
### Review 2  
After the basic Docker materials were put together, the risks shifted towards maintaining a stable app on the live site. These risks were countered by using Docker swarm across multiple EC2s for enhanced durability, and by including a test stage in the Jenkins build, so to prevent malfunctioning updated from being deployed to the live site.
![Imgur](https://i.imgur.com/TNDYNpb.png)

<br><br>

# 3 Creation of AWS structure

## VPC, Subnets and Security Groups Created
* VPC: a VPC with CIDR 10.0.0.0/16 was set up.
* Separate security groups for EC2 and RDS created:
  * EC2 instance security, allowing traffic from:
    * All sources on port 80 (for nginx), 5000 (for the frontend container), and 8080 (for Jenkins)
    * Devs' public IPs on port 22 for SSH
    * Within the VPC for other ports required by the app or by Docker swarm.
  ![Imgur](https://i.imgur.com/vMYyHN8.png)
  * Database security, allowing traffic only from within the VPC on port 3306.
  ![Imgur](https://i.imgur.com/gLB7NMn.png)


## EC2 and RDS instances set up
* RDS mysql created and given database security group.
* 3 EC2 instances created: one for the manager of the swarm, two others to be workers. Only manager EC2 used until swarm set up (below).
![Imgur](https://i.imgur.com/bx43G85.png)
<br><br>

# 4 Microservice setup
## SSH into EC2 instance, install Docker and Docker-Compose
## Basic Services set up:
### Materials for Docker containers for each microservice created:
* **Nginx**: ```nginx.conf``` file set up to run as reverse proxy, redirecting http traffic on port 80 to the EC2's IP address at port 5000, where the Flask app frontend is set to listen.  
![Imgur](https://i.imgur.com/GVg300D.png)  
(The address for the proxy pass was later was directed to the frontend app using the Docker Swarm Stack DNS rather than the IP address.)
<br><br>
* **Flask App Frontend**  
The frontend app required python and the files specified in the requirements.txt file; investigation of app.py showed that it needed port 5000 exposed.  
![Imgur](https://i.imgur.com/G3R3ITn.png)  
(The ```routes.py``` file for the frontend was later updated so that the http request was directed to the backend app using the Docker Swarm Stack DNS.)
<br><br>
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
<br><br>
# 5 Docker-compose
A docker-compose.yaml could then be created, referring to the Dockerfiles created above for the build stage.  
![Imgur](https://i.imgur.com/zDRTFEH.png)  
At this stage, as not currently using Docker Swarm, container_name was set for the frontend and backend services.
<br><br>

# 6 Docker swarm stack
## Swarm created
Swarm created on the manager EC2 using the command ```docker swarm init```; the other two EC2s were connected to the swarm using the token provided.  
![Imgur](https://i.imgur.com/Jlc5NOB.png)

## Images uploaded to Docker hub
Custom Docker images for the frontend and backend were pushed to DockerHub, so that they can be accessed from any EC2 instance.  
![Imgur](https://i.imgur.com/lAlryI2.png)

## docker-compose.yaml edited
Then the docker-compose.yaml was edited to ensure that the images specified were those on Docker. The number of replicas for the swarm stack to build was also specified.  
![Imgur](https://i.imgur.com/msVaQeB.png)  

## Stack 
The stack was then deployed using ```docker stack deploy --compose-file docker-compose.yaml project-stack```. Containers were then deployed across the three EC2 instances in the swarm: 
![Imgur](https://i.imgur.com/FpwFFpb.png)
<br><br>

# 7 Jenkins  

## Pipeline created, associated with Github repo
![Imgur](https://i.imgur.com/e0Msn5M.png)
Github repo is available [here](https://github.com/TomWhite46/DevOps-Project).

## Jenkinsfile on Github set up to deploy Docker stack on EC2:
The deployment stage runs docker stack as had previously been done directly on the EC2 instance. This included a build stage - so that any new edits to the app would be pushed to the images on Dockerhub - and a deploy stage.  
![Imgur](https://i.imgur.com/Zyu8Q66.png)

Note that credentials were set up as secrets in Jenkins in order to protect the database password.
![Imgur](https://i.imgur.com/SFHCDQ8.png)

## Webhook set up
![Imgur](https://i.imgur.com/m19wcgU.png)  
Commits to main on Github now caused automatic rebuild on Jenkins.
<br><br>

# 8 Python testing with pytest  
Python3 installed on EC2 instance, and script for python tests added to Jenkinsfile.  
![Imgur](https://i.imgur.com/N1f0FeS.png)  
On committing the updated Jenkinsfile to Github, the tests were run as part of the automatically triggered Jenkins build, showing a successful result.  
![Imgur](https://i.imgur.com/WE3oMv2.png)  
Looking at the console output on Jenkins shows 100% test coverage for both frontend and backend:  
* Frontend:  
![Imgur](https://i.imgur.com/QvNolPY.png)
* Backend:  
![Imgur](https://i.imgur.com/0HnooEp.png)
<br><br>

# 9 Final test build: edit made to index.html: 
Edit made to index.html: inserted word 'many' in line 3:
![Imgur](https://i.imgur.com/i0Z0ifA.png)  
Successful build on Jenkins:  
![Imgur](https://i.imgur.com/BKpaJ1S.png)  
Edit to file reflected on webpage at EC2's public IP:  
![Imgur](https://i.imgur.com/AiNInXO.png)
<br><br>

# 10 Stretch goal: deployment to separate dev site from dev branch
Deploying modified builds to a non-production environment is an needed in order to ensure that the whole build works as expected before pushing it the main branch and deploying to the public site.  
To achieve this, an additional EC2 instance was created with slightly different security rules - allowing access on port 80 only from the devs' IP addresses, to prevent public access.  
The original EC2 rule group was broken up into the rules needed for all dev and prod EC2s on the one hand, and a separate group opening port 80 to all incoming traffic for the live EC2s. That allowed the 'ec2-security' group to be reused for the EC2 running the dev environment, so that all that was needed was an additional group allowing HTTP traffic from the devs' IPs.  
![Imgur](https://i.imgur.com/tPe3B31.png)  
A new Jenkins pipeline was then created on the dev EC2 instance, pointing to the dev branch on the Github repo.  
![Imgur](https://i.imgur.com/T1Z3tqr.png)  
An additional webhook was set up on Github:  
![Imgur](https://i.imgur.com/pgmC5r5.png)  
Making a commit to the dev branch on Github now causes the dev EC2's Jenkins to run the build, allowing any code changes to be tested directly on that environment before being deployed to the public-facing EC2s.
<br><br>

# 11 Further Goals
* Add an extra EC2 to the Docker swarm as an additional manager, to increase durability of the infrastructure in the event of the manager EC2 going down.
<br><br>

# 12 Acknowledgements
Credit to Luke Benson for the tuition, Jordan H for the commentary in Teams chat, and BAE-12 Team 4 for emotional support.
<br><br><br>
## Project by Emily Penrice and Tom White