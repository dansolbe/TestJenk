pipeline {
    agent any

    environment {
        BASE_URL = 'https://cloud-api.yandex.net/v1/disk'
        RESOURCE_ENDPOINT = 'resources'
        TRASH_ENDPOINT = 'trash/resources'
        OAUTH_TOKEN = credentials('Ya_disk_token')
        ALLURE_VERSION = '2.13.8'
    }

    stages {
        stage('Install Python, Allure and uv') {
            steps {
                sh '''
                    # Install system dependencies
                    apt-get update && apt-get install -y python3 curl unzip

                    # Install uv
                    curl -LsSf https://astral.sh/uv/install.sh | sh
                    export PATH="$HOME/.local/bin:$PATH"

                    # Install Allure directly in the workspace (current directory)
                    echo "Installing Allure ${ALLURE_VERSION}..."

                    if [ ! -d "allure-${ALLURE_VERSION}" ]; then
                        curl -Lo allure.zip "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.zip"
                        unzip -q allure.zip
                        rm allure.zip
                        chmod -R 755 "allure-${ALLURE_VERSION}"
                    fi

                    # Verify installation
                    "./allure-${ALLURE_VERSION}/bin/allure" --version
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
                    export PATH="$HOME/.local/bin:$PATH"
                    uv run pytest --alluredir=allure_results
                '''
            }
        }
    }

    post {
        always {
            script {
                // Use Allure from the workspace
                allure commandline: "allure-${ALLURE_VERSION}",
                       includeProperties: false,
                       results: [[path: 'allure_results']],
                       report: 'allure_report'
            }
        }
    }
}
