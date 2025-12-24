pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        PYTHON = "${env.WORKSPACE}/venv/bin/python"
        PIP = "${env.WORKSPACE}/venv/bin/pip"
    }

    stages {

        stage('Setup Python Environment') {
            steps {
                sh '''
                # Create virtual environment if it doesn't exist
                if [ ! -d "${VENV_DIR}" ]; then
                    python3 -m venv ${VENV_DIR}
                fi

                # Upgrade pip and install requirements
                ${PIP} install --upgrade pip
                ${PIP} install -r requirements.txt
                '''
            }
        }

        stage('Migrate Database') {
            steps {
                sh '''
                # Run Django migrations
                ${PYTHON} manage.py migrate
                '''
            }
        }

        stage('Collect Static Files') {
            steps {
                sh '''
                # Collect static files
                ${PYTHON} manage.py collectstatic --noinput
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                # Run Django tests
                ${PYTHON} manage.py test
                '''
            }
        }

    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs.'
        }
    }
}

