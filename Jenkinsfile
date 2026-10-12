
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'allfridhosaragi/flask-docker-database'
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
                bat 'docker buildx build --load -t %IMAGE_NAME%:%BUILD_NUMBER% .'
                bat 'docker image inspect %IMAGE_NAME%:%BUILD_NUMBER%'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-v2',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    powershell '''
                        $ErrorActionPreference = "Stop"

                        $configDir = Join-Path $env:TEMP (
                            "jenkins-docker-" + [guid]::NewGuid().ToString("N")
                        )

                        try {
                            New-Item -ItemType Directory -Force -Path $configDir | Out-Null

                            $pair = "$($env:DOCKER_USER):$($env:DOCKER_TOKEN)"
                            $auth = [Convert]::ToBase64String(
                                [Text.Encoding]::UTF8.GetBytes($pair)
                            )

                            $config = @{
                                auths = @{
                                    "https://index.docker.io/v1/" = @{
                                        auth = $auth
                                    }
                                }
                            } | ConvertTo-Json -Depth 5

                            [System.IO.File]::WriteAllText(
                                (Join-Path $configDir "config.json"),
                                $config,
                                (New-Object System.Text.UTF8Encoding($false))
                            )

                            $env:DOCKER_CONFIG = $configDir

                            $image = "$($env:IMAGE_NAME):$($env:BUILD_NUMBER)"
                            $latest = "$($env:IMAGE_NAME):latest"

                            Write-Host "Push image versi build..."

                            docker push $image

                            if ($LASTEXITCODE -ne 0) {
                                throw "Push image versi build gagal"
                            }

                            Write-Host "Membuat tag latest..."

                            docker tag $image $latest

                            if ($LASTEXITCODE -ne 0) {
                                throw "Docker tag gagal"
                            }

                            Write-Host "Push image latest..."

                            docker push $latest

                            if ($LASTEXITCODE -ne 0) {
                                throw "Push latest gagal"
                            }

                            Write-Host "Seluruh Docker Push berhasil!"
                        }
                        finally {
                            $env:DOCKER_CONFIG = $null
                            Remove-Item -Recurse -Force $configDir -ErrorAction SilentlyContinue
                        }
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline berhasil!'
        }
        failure {
            echo 'Pipeline gagal. Periksa Console Output.'
        }
        always {
            echo 'Proses Pipeline selesai.'
        }
    }
}
