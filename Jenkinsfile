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
                    sh "python3 -m pytest --cov application"
                    sh "cd /home/jenkins/.jenkins/workspace/project-pipeline/backend"
                    sh "pip3 install -r requirements.txt"
                    sh "python3 -m pytest --cov application"
                }
            }
                stage('Run docker'){
                steps{
                    sh "cd /home/jenkins/.jenkins/workspace/project-pipeline"
                    sh "docker-compose up -d --build"
                }
            }

        }
}
