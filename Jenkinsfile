pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'weather-predictor'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/ -v --tb=short --cov=app --cov-report=xml --cov-report=html
                '''
            }
            post {
                always {
                    // Publish test results
                    junit '**/test-results.xml'
                    // Publish coverage report
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')]
                }
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install safety
                    safety check
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Docker Test') {
            steps {
                sh '''
                    # Run container and test health endpoint
                    docker run -d --name weather-test -p 5001:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                    sleep 10
                    curl -f http://localhost:5001/health || exit 1
                    docker stop weather-test
                    docker rm weather-test
                '''
            }
        }

        stage('Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials',
                                                 usernameVariable: 'DOCKER_USERNAME',
                                                 passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                        echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    # Deploy to staging environment
                    # This could be docker-compose, kubernetes, etc.
                    echo "Deploying to staging..."
                    # docker-compose up -d
                '''
            }
        }
    }

    post {
        always {
            // Clean up
            sh 'docker system prune -f'
            // Archive artifacts
            archiveArtifacts artifacts: 'coverage.html', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}