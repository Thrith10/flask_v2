pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Thrith10/FlaskDemo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('my-flask-app:latest', '-f Dockerfile.flask .')
                }
            }
        }

        stage('Prepare Scripts') {
            steps {
                sh 'git update-index --chmod=+x jenkins/scripts/deploy.sh'
                sh 'git update-index --chmod=+x jenkins/scripts/kill_integration.sh'
            }
        }

        stage('Install Dependencies') {
            agent {
                docker {
                    image 'python:latest'
                    args '-u root'
                }
            }
            steps {
                sh 'pip install pytest pytest-cov selenium webdriver-manager'
            }
        }

        stage('Run Unit Tests') {
            agent {
                docker {
                    image 'python:latest'
                    args '-u root'
                }
            }
            steps {
                sh 'mkdir -p logs'
                script {
                    try {
                        sh 'pytest --junitxml=logs/unitreport.xml tests/'
                    } catch (Exception e) {
                        echo "pytest failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
            post {
                always {
                    junit testResults: 'logs/unitreport.xml', allowEmptyResults: true
                }
            }
        }

        stage('Integration UI Test') {
            parallel {
                stage('Headless Browser Test') {
                    agent {
                        docker {
                            image 'python:3.9' // or whichever version you're using
                            args '-u root'
                        }
                    }
                    steps {
                        sh '''
                            pip install selenium webdriver-manager pytest flask
                            apt-get update
                            apt-get install -y wget unzip --fix-missing || apt-get install -y wget unzip --fix-missing
                            wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
                            apt install -y ./google-chrome-stable_current_amd64.deb
                            wget https://chromedriver.storage.googleapis.com/$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
                            unzip -o chromedriver_linux64.zip
                            mv chromedriver /usr/local/bin/
                        '''
                        sh 'mkdir -p logs'
                        script {
                            try {
                                sh 'pytest test_app.py --junitxml=logs/integration_test_results.xml'
                            } catch (Exception e) {
                                echo "Integration tests failed: ${e.message}"
                                currentBuild.result = 'FAILURE'
                            }
                        }
                    }
                    post {
                        always {
                            junit 'logs/integration_test_results.xml'
                        }
                    }
                }
                stage('Deploy') {
                    steps {
                        sh './jenkins/scripts/deploy.sh'
                        input message: 'Finished using the web site? (Click "Proceed" to continue)'
                        sh './jenkins/scripts/kill_integration.sh'
                    }
                }
            }
        }

        stage('Code Quality Check via SonarQube') {
            steps {
                script {
                    def scannerHome = tool 'SonarQube_Flask'
                    withSonarQubeEnv('SonarQube_Flask') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=FlaskDemo -Dsonar.sources=."
                    }
                }
            }
        }
    }

    post {
        always {
            junit testResults: 'logs/**/*.xml', allowEmptyResults: true
            recordIssues enabledForFailure: true, tool: sonarQube()
        }
    }
}
