pipeline{
        agent any
        environment {
            DB_URI = credentials('DB_link')
            SECR_KEY = credentials('Secret_Key')
        }
        stages{
            stage('Build'){
                steps{
                    sh "docker login -u tomrwhite -p Miltiades!490 && cd ./frontend && docker build -t docker.io/tomrwhite/frontend-image:latest . && docker push docker.io/tomrwhite/frontend-image:latest"
                    sh "cd ./backend && docker build -t docker.io/tomrwhite/backend-image:latest . && docker push docker.io/tomrwhite/backend-image:latest"
                }
            }
            stage('Testing'){
                steps{
                    sh "cd ./frontend && pip3 install -r requirements.txt  && python3 -m pytest"
                    sh "cd ./backend && pip3 install -r requirements.txt && python3 -m pytest"
                }
            }
                stage('Run docker'){
                steps{
                    // sh "docker-compose up -d --build
                    sh "docker stack deploy --compose-file docker-compose.yaml project-stack"
                }
            }

        }
}
