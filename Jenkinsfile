pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        ECR_REGISTRY = "321869098564.dkr.ecr.ap-south-1.amazonaws.com"
        ECR_REPOSITORY = "usermanagement"
        IMAGE = "${ECR_REGISTRY}/${ECR_REPOSITORY}"
        CONTAINER_NAME = "django_app"
        PORT = "8000"
        WORKSPACE_DIR = "${env.WORKSPACE}/tmp_env"
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
                    mkdir -p ${WORKSPACE_DIR}
                    cp \$ENVFILE ${WORKSPACE_DIR}/.env
                    echo '.env loaded in ${WORKSPACE_DIR}'
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE}:latest ."
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-creds', 
                                                  usernameVariable: 'AWS_ACCESS_KEY_ID', 
                                                  passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                    aws configure set aws_access_key_id \$AWS_ACCESS_KEY_ID
                    aws configure set aws_secret_access_key \$AWS_SECRET_ACCESS_KEY
                    aws configure set region ${AWS_REGION}
                    aws ecr get-login-password | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                    """
                }
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh "docker push ${IMAGE}:latest"
            }
        }

        stage('Deploy on EC2') {
            steps {
                sh """
                echo "Stopping old container if exists"
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true

                echo "Pulling latest image"
                docker pull ${IMAGE}:latest

                echo "Starting new container"
                docker run -d --name ${CONTAINER_NAME} \
                    --env-file ${WORKSPACE_DIR}/.env \
                    -p ${PORT}:8000 \
                    ${IMAGE}:latest
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

