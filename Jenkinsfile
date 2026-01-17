pipeline {
    agent any

    tools {
        allure 'allure'
    }

    environment {
        BASE_URL = 'https://cloud-api.yandex.net/v1/disk'
        RESOURCE_ENDPOINT = 'resources'
        TRASH_ENDPOINT = 'trash/resources'
        OAUTH_TOKEN = credentials('Ya_disk_token')
    }

    stages {
        stage('Install Python and uv') {
            steps {
                sh '''
                    apt-get update && apt-get install -y python3 curl
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
                    uv run pytest --alluredir=allure_results
                '''
            }
        }
    }

    post {
        always {
            allure includeProperties: false,
                   results: [[path: 'allure_results']],
                   //report: 'allure_report',
                   //reportName: "Allure Report - Build $BUILD_NUMBER",
                   //reportBuildPolicy: 'ALWAYS'
        }
    }
}
