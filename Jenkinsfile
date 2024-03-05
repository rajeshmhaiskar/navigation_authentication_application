pipeline{
    agent {label "dev"}
    stages{
        stage("Clone Code"){
            steps{
                git url: "https://github.com/rajeshmhaiskar/navigation_authentication_application.git", branch: "main"
            }
        }
        stage("Build and Test") {
            steps{
                sh "docker build . -t nav-auth"
            }
        }
        stage("Login and Push image")
        {
            steps{
                withCredentials([usernamePassword(credentialsId:"dockerhub",passwordVariable:"Mhaiskar143",usernameVariable:"mhaiskarrajesh25")]){
                    sh """
                    #!/bin/sh
                    docker tag nav-auth ${env.dockerhubUsername}/nav-auth:latest
                    docker login -u ${env.dockerhubUsername} -p ${env.dockerhubPassword}
                    docker push ${env.dockerhubUsername}/nav-auth:latest
                    """
                }
            }
        }
        stage("Deploy") {
            steps{
                sh "docker-compose down && docker-compose up -d"
            }
        }
    }
}
