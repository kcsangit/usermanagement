pipeline {
  agent any
  stages {
    stage('Setup') {
      steps {
        sh '''
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        '''
      }
    }
    stage('Migrate & Collect Static') {
      steps {
        sh '''
        source venv/bin/activate
        python manage.py migrate
        '''
      }
    }
  }
}

