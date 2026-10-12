
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'allfridhosaragi/flask-docker-database'
        DOCKER_CONFIG = "${WORKSPACE}\\.docker"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Mengambil source code GitHub'
                checkout scm
            }
        }

        stage('Check Docker') {
            steps {
                bat 'docker --version'
                bat 'docker info --format "{{.ServerVersion}}"'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker buildx build --load -t %IMAGE_NAME%:%BUILD_NUMBER% .'
                bat 'docker image inspect %IMAGE_NAME%:%BUILD_NUMBER% --format "{{.Id}}"'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    powershell '''
                        $ErrorActionPreference = "Stop"
                        $env:DOCKER_TOKEN | docker login -u $env:DOCKER_USER --password-stdin
                        if ($LASTEXITCODE -ne 0) {
                            throw "Docker Hub login gagal"
                        }
                    '''
                    bat 'docker push %IMAGE_NAME%:%BUILD_NUMBER%'
                    bat 'docker tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:latest'
                    bat 'docker push %IMAGE_NAME%:latest'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline Docker berhasil!'
        }
        failure {
            echo 'Pipeline Docker gagal. Periksa Console Output.'
        }
        always {
            bat 'docker logout'
            echo 'Proses Pipeline selesai.'
        }
    }
}
