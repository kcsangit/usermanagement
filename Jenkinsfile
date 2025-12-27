pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        ECR_REGISTRY = "321869098564.dkr.ecr.ap-south-1.amazonaws.com"
        ECR_REPOSITORY = "usermanagement"
        IMAGE = "${ECR_REGISTRY}/${ECR_REPOSITORY}"
        CONTAINER_NAME = "django_app"
        PORT = "8000"
    }

    stages {

        // 1️⃣ Checkout code from GitHub (master branch)
        stage('Checkout Code') {
            steps {
                git branch: 'master', url: 'https://github.com/kcsangit/usermanagement.git'
            }
        }

        // 2️⃣ Inject .env secret safely into workspace
        stage('Inject .env Secret') {
            steps {
                withCredentials([file(credentialsId: 'django-env', variable: 'ENVFILE')]) {
                    sh '''
                    mkdir -p $WORKSPACE/tmp_env
                    cp $ENVFILE $WORKSPACE/tmp_env/.env
                    echo ".env loaded in $WORKSPACE/tmp_env"
                    '''
                }
            }
        }

        // 3️⃣ Build Docker image
        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${IMAGE}:latest .
                """
            }
        }

        // 4️⃣ Login to AWS ECR using AWS Credentials plugin
        stage('Login to AWS ECR') {
            steps {
                withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
                    sh """
                    aws ecr get-login-password --region ${AWS_REGION} \
                    | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                    """
                }
            }
        }

        // 5️⃣ Push Docker image to AWS ECR
        stage('Push Image to ECR') {
            steps {
                sh """
                docker push ${IMAGE}:latest
                """
            }
        }

        // 6️⃣ Deploy container on EC2
        stage('Deploy on EC2') {
            steps {
                sh """
                echo "Stopping old container if exists..."
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true

                echo "Pulling latest image..."
                docker pull ${IMAGE}:latest

                echo "Starting new container..."
                docker run -d --name ${CONTAINER_NAME} \
                    --env-file $WORKSPACE/tmp_env/.env \
                    -p ${PORT}:8000 \
                    ${IMAGE}:latest
                """
            }
        }
    }

    post {
        success {
            echo "🎉 Deployment Successful"
        }
        failure {
            echo "❌ Deployment Failed"
        }
    }
}

