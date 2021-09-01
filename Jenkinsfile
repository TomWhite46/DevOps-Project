pipeline{
        agent any
        environment {
            DB_URI = credentials('DB_link')
            SECR_KEY = '1234'
        }
        stages{
            stage('Run docker'){
                steps{
                    sh "cd /home/jenkins/.jenkins/workspace/project-pipeline"
                    sh "docker-compose up -d --build"
                }
            }
            stage('Make Files'){
                steps{
                    sh "echo 'hello'"
                }
            }
        }
}
