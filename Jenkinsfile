pipeline {
    agent { label 'agent1' }
    environment {
        VENV = '/home/user1/workspace/venv'
    }
    stages {
        stage('local setup') {
            steps {
                sh 'node --version'
                sh 'npm --version'
                sh 'zowe --version'
                sh 'zowe plugins list'
                sh 'python3 -m venv $VENV --clear'
                sh '$VENV/bin/python -m pip install --no-index --find-links ./duty-offline-install/wheelhouse-linux-py313/ duty==1.9.0 dotmap==1.3.30'
            }
        }
        stage('build') {
            steps {
                sh 'echo build'
            }
        }
        stage('run') {
            steps {
                sh 'echo run'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'output/**/*.*'
        }
    }
}
