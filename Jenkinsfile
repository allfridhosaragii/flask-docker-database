
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'allfridhosaragi/flask-docker-database'
        DOCKER_CONFIG = "${WORKSPACE}\\.docker"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Mengambil source code dari GitHub'
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
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    bat '''
                        echo %DOCKER_TOKEN% | docker login -u %DOCKER_USER% --password-stdin
                        docker push %IMAGE_NAME%:%BUILD_NUMBER%
                        docker tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:latest
                        docker push %IMAGE_NAME%:latest
                        docker logout
                    '''
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
            echo 'Proses Pipeline selesai.'
        }
    }
}
