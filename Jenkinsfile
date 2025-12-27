pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        ECR_REGISTRY = "321869098564.dkr.ecr.ap-south-1.amazonaws.com"
        ECR_REPOSITORY = "usermanagement"
        IMAGE = "${ECR_REGISTRY}/${ECR_REPOSITORY}"
        PORT = "8000"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'master', url: 'https://github.com/kcsangit/usermanagement.git'
            }
        }

        stage('Inject .env Secret') {
            steps {
                withCredentials([file(credentialsId: 'django-env', variable: 'ENVFILE')]) {
                    sh """
                    mkdir -p "\$WORKSPACE/tmp_env"
                    cp "\$ENVFILE" "\$WORKSPACE/tmp_env/.env"
                    cp "\$WORKSPACE/tmp_env/.env" "\$WORKSPACE/.env"
                    echo '.env loaded'
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${IMAGE}:latest .
                """
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-creds', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                    aws ecr get-login-password --region ${AWS_REGION} \
                    | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                    """
                }
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh """
                docker tag ${IMAGE}:latest ${IMAGE}:latest
                docker push ${IMAGE}:latest
                """
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh """
                docker-compose down || true
                docker-compose pull
                docker-compose up -d
                """
            }
        }
    }

    post {
        success {
            echo "Deployment Successful"
        }
        failure {
            echo "Deployment Failed"
        }
    }
}

