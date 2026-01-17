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
                    # Fix permissions
                    sudo chmod 755 /var/lib/apt/lists/ || true
                    apt-get update && apt-get install -y python3 curl unzip

                    # Install uv
                    curl -LsSf https://astral.sh/uv/install.sh | sh
                    export PATH="$HOME/.local/bin:$PATH"

                    # Install Allure manually to the expected Jenkins location
                    echo "Installing Allure ${ALLURE_VERSION}..."
                    ALLURE_INSTALL_DIR="/var/jenkins_home/tools/ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation/allure"
                    sudo mkdir -p /var/jenkins_home/tools/ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation/

                    if [ ! -d "$ALLURE_INSTALL_DIR" ]; then
                        curl -Lo allure.zip "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.zip"
                        unzip -q allure.zip -d /tmp/
                        sudo mv /tmp/allure-${ALLURE_VERSION} "$ALLURE_INSTALL_DIR"
                        rm allure.zip
                        echo "Allure installed to $ALLURE_INSTALL_DIR"
                    else
                        echo "Allure already installed at $ALLURE_INSTALL_DIR"
                    fi

                    # Verify installation
                    if [ -f "$ALLURE_INSTALL_DIR/bin/allure" ]; then
                        echo "Allure installation successful"
                        $ALLURE_INSTALL_DIR/bin/allure --version
                    else
                        echo "Allure installation failed"
                        ls -la "$ALLURE_INSTALL_DIR" || true
                    fi

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
                // Verify Allure is accessible
                sh '''
                    ALLURE_PATH="/var/jenkins_home/tools/ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation/allure/bin/allure"
                    if [ -f "$ALLURE_PATH" ]; then
                        echo "Allure commandline found at: $ALLURE_PATH"
                        $ALLURE_PATH --version
                    else
                        echo "ERROR: Allure commandline not found!"
                        # Try to find it anywhere
                        find /var/jenkins_home/tools/ -name "allure" -type f 2>/dev/null || true
                    fi
                '''

                // Use the allure step - it should now find the installed tool
                allure includeProperties: false,
                       results: [[path: 'allure_results']],
                       report: 'allure_report'
            }
        }
    }
}

