pipeline{
        agent any
        environment {
            DB_URI = credentials('DB_link')
            SECR_KEY = credentials('Secret_Key')
        }
        stages{
            stage('Testing'){
                steps{
                    sh "cd /home/jenkins/.jenkins/workspace/project-pipeline/frontend"
                    sh "pip3 install -r /home/jenkins/.jenkins/workspace/project-pipeline/frontend/requirements.txt"
                    sh "cd /home/jenkins/.jenkins/workspace/project-pipeline/frontend && python3 -m pytest"
                    sh "cd /home/jenkins/.jenkins/workspace/project-pipeline/backend"
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
