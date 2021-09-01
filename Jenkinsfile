pipeline{
        agent any
        stages{
            stage('Run docker'){
                steps{
                    sh "cd /home/jenkins/.jenkins/workspace/project-pipeline"
                    sh "docker-compose up -d"
                }
            }
            stage('Make Files'){
                steps{
                    sh "echo 'hello'"
                }
            }
        }
}
