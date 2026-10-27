pipeline {
    agent any
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
    }
    post {
        success {
            echo 'V1 build and tests completed successfully.'
        }
        failure {
            echo 'V1 pipeline failed. Check the Console Output.'
        }
    }
}
