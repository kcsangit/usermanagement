pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/kcsangit/usermanagement'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t django-app .'
            }
        }

        stage('Run with Docker Compose') {
            steps {
                sh 'docker compose up -d --build'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker exec django_app python manage.py test'
            }
        }

    }

    post {
        always {
            sh 'docker compose down'
        }
    }
}

