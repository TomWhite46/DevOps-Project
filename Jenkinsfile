pipeline{
        agent any
        stages{
            stage('Run docker'){
                steps{
                    sh "DB_URI='mysql+pymysql://admin:WeLoveLuke@project-database.cyknho36mb9t.eu-west-1.rds.amazonaws.com:3306/users'"
                    sh "export DB_URI"
                    sh "SECR_KEY='1234'"
                    sh "export SECR_KEY"
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
