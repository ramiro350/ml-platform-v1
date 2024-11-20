pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'ml-predict-api'
        // REPO_URL = 'https://github.com/antonio-marcos1989/ml-platform-v1.git'
    }
    stages {
        // stage('Clone Repository') {
        //     steps {
        //         git branch: 'main', url: "${REPO_URL}"
        //     }
        // }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }
        stage('Run Docker Container') {
            steps {
                sh "docker run -d -p 5001:5001 ${DOCKER_IMAGE}"
            }
        }
    }
    post {
        always {
            script {
                // Stop and clean up running containers with the same image
                def containerIds = sh(script: "docker ps -q --filter ancestor=${DOCKER_IMAGE}", returnStdout: true).trim()
                if (containerIds) {
                    sh "docker stop ${containerIds}"
                }
            }
        }
    }
}
