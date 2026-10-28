
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'harivarsan1177/todoapp'
        IMAGE_TAG = 'v1'
        DOCKER = 'C:\\Users\\ASUS\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'V1 source code checked out from GitHub'
            }
        }

        stage('Check Python') {
            steps {
                bat 'python --version'
                bat 'python -m pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m unittest discover -s tests -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '"%DOCKER%" build -t %DOCKER_IMAGE%:%IMAGE_TAG% .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat 'echo %DOCKERHUB_TOKEN% | "%DOCKER%" login -u %DOCKERHUB_USERNAME% --password-stdin'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                bat '"%DOCKER%" push %DOCKER_IMAGE%:%IMAGE_TAG%'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: V1 tests passed and Docker image was pushed to Docker Hub.'
        }

        failure {
            echo 'FAILURE: Check Console Output for the exact error.'
        }
    }
}
