pipeline{
        agent any
        environment {
            DB_URI = credentials('DB_link')
            SECR_KEY = credentials('Secret_Key')
        }
        stages{
            stage('Testing'){
                steps{
                    sh "cd /home/jenkins/.jenkins/workspace/project-pipeline/frontend && pip3 install -r requirements.txt  && python3 -m pytest
                    sh "pip3 install -r /home/jenkins/.jenkins/workspace/project-pipeline/backend/requirements.txt"
                    sh "cd /home/jenkins/.jenkins/workspace/project-pipeline/backend && python3 -m pytest"
                }
            }
                stage('Run docker'){
                steps{
                    sh "cd /home/jenkins/.jenkins/workspace/project-pipeline && docker-compose up -d --build"
                }
            }

        }
}
