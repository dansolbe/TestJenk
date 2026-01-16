pipeline {
    agent any

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
                    apt-get update && apt-get install -y python3 python3-pip curl
                    curl -LsSf https://astral.sh/uv/install.sh | sh
                    export PATH="$HOME/.local/bin:$PATH"
                '''
            }
        }

        stage('Create .env file') {
            steps {
                sh '''
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

        stage('Run tests with allure') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    uv run pytest --alluredir=allure_results
                '''
            }
        }
    }

    post {
        always {
            allure results: [[path: "allure_results"]]
            archiveArtifacts artifacts: "allure_results/**/*", fingerprint: true
        }
    }
}
