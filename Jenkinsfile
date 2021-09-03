pipeline{
        agent any
        environment {
            DB_URI = credentials('DB_link')
            SECR_KEY = credentials('Secret_Key')
            DOCKER_PW = credentials('Docker_PW')
            DOCKER_USER = credentials('Docker_user')
        }
        stages{
            stage('Build'){
                steps{
                        sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PW} && cd ./frontend && docker build -t docker.io/tomrwhite/frontend-image:latest . && docker push docker.io/tomrwhite/frontend-image:latest"
                        sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PW} && cd ./backend && docker build -t docker.io/tomrwhite/backend-image:latest . && docker push docker.io/tomrwhite/backend-image:latest"
                }
            }
            stage('Testing'){
                steps{
                    sh "cd ./frontend && pip3 install -r requirements.txt  && python3 -m pytest --cov-report application"
                    sh "cd ./backend && pip3 install -r requirements.txt && python3 -m pytest --cov application"
                }
            }
                stage('deploy'){
                steps{
                    // sh "docker-compose up -d --build
                    sh "docker stack deploy --compose-file docker-compose.yaml project-stack"
                    sh "echo 'hello'"
                }
            }

        }
}
