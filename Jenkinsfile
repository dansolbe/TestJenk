pipeline {
    agent any

    environment {
        BASE_URL = 'https://cloud-api.yandex.net/v1/disk'
        RESOURCE_ENDPOINT = 'resources'
        TRASH_ENDPOINT = 'trash/resources'
        OAUTH_TOKEN = credentials('Ya_disk_token')
        ALLURE_DIR = 'allure_results'
        ALLURE_HISTORY_DIR = 'allure_history'
    }

    stages {
        stage('Install Python, allure and uv') {
            steps {
                sh '''
                    apt-get update && apt-get install -y python3 python3-pip curl wget tar
                    wget https://github.com/allure-framework/allure2/releases/download/2.25.0/allure-2.25.0.tgz
                    tar -xzf allure-2.13.8.tgz
                    export PATH="$PWD/allure-2.13.8/bin:$PATH"
                    allure --version
                    curl -LsSf https://astral.sh/uv/install.sh | sh
                    export PATH="$HOME/.local/bin:$PATH"
                    uv --version
                '''
            }
        }
        stage('Create .env file') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    echo "BASE_URL=$BASE_URL" > .env
                    echo "OAUTH_TOKEN=$OAUTH_TOKEN" >> .env
                    echo "RESOURCE_ENDPOINT=$RESOURCE_ENDPOINT" >> .env
                    echo "TRASH_ENDPOINT=$TRASH_ENDPOINT" >> .env
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    uv sync
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PWD/allure-2.13.8/bin:$PATH"
                    uv run pytest --alluredir=$ALLURE_DIR
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh '''
                    export PATH="$PWD/allure-2.13.8/bin:$PATH"
                    mkdir -p $ALLURE_HISTORY_DIR
                    allure generate --clean $ALLURE_DIR -o allure_report --report-dir $ALLURE_HISTORY_DIR/$BUILD_NUMBER
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: '$ALLURE_HISTORY_DIR/$BUILD_NUMBER/**/*', fingerprint: true
                }
            }
        }
    }

    post {
        always {
            allure includeProperties: false,
                   results: [[path: 'allure_results']],
                   reportDir: 'allure_report',
                   reportName: "Allure Report - Build $BUILD_NUMBER",
                   reportBuildPolicy: 'ALWAYS'
        }
    }
}
