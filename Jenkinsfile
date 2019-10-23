def build_number = env.BUILD_URL
def customMetrics = [:]
def customMetricsMap = [:]

pipeline{
    agent {
        label 'ci-pipeline-jenkins-slave'
    }
    stages {
        stage('Preparation') {
            steps {
                script {
                    customMetricsMap["jenkins_data"] = customMetrics
                    checkout scm
                }
            }
        }
        stage('Get Foundations Scheduler') {
            steps {
                container("python3") {
                    sh 'python -m pip install -U foundations-scheduler'
                }
            }
        }
        stage('Foundations Install Test Requirements') {
            steps {
                container("python3") {
                    sh "./ci_install_requirements.sh"
                }
            }
        }
        stage('Build Foundations Wheels') {
            steps {
                container("python3") {
                    sh "./build_dist.sh"
                }
            }
        }
        stage('Run Unit Tests') {
            steps {
                container("python3") {
                    sh "./run_unit_tests.sh"
                }
            }
        }
        stage('Build Images and Push to Testing Env') {
            failFast true
            parallel{
                stage('Build Model Package Image and Push to Testing Env') {
                    stages {
                        stage('Build Model Package Image and Push to Testing Env') {
                            steps {
                                container("python3") {
                                    ws("${WORKSPACE}/foundations_model_package/src"){
                                        sh 'docker login docker.shehanigans.net -u $NEXUS_USER -p $NEXUS_PASSWORD'
                                        sh 'docker login docker-staging.shehanigans.net -u $NEXUS_USER -p $NEXUS_PASSWORD'
                                        sh './build.sh'
                                        sh 'docker push docker-staging.shehanigans.net/foundations-model-package:latest'
                                        sh './pull_staging_image_onto_scheduler.sh'
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Build Worker Images and Push to Testing Env') {
                    stages {
                        stage('Build Worker Images and Push to Testing Env') {
                            steps {
                                container("python3-1") {
                                    sh 'docker login docker.shehanigans.net -u $NEXUS_USER -p $NEXUS_PASSWORD'
                                    sh 'docker login docker-staging.shehanigans.net -u $NEXUS_USER -p $NEXUS_PASSWORD'
                                    sh './build_worker_images.sh '
                                }
                            }
                        }
                    }
                }
            }
        }
        stage('Run Integration Tests and Prepare for Acceptance Tests'){
            failFast true
            parallel{
                stage('Run Integration Tests') {
                    stages {
                        stage('Run Integration Tests') {
                            steps {
                                container("python3") {
                                    sh 'export FOUNDATIONS_SCHEDULER_HOST=$FOUNDATIONS_SCHEDULER_ACCEPTANCE_HOST && ./run_integration_tests.sh'
                                }
                            }
                        }
                    }
                }
                stage('Install Foundations (container 1)') {
                    stages{
                        stage('Install Foundations (container 1)'){
                            steps {
                                container("python3-1") {
                                    ws("${WORKSPACE}/testing") {
                                        sh 'python -m pip install ../dist/*.whl'
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Install Foundations (container 2)') {
                    stages{
                        stage('Install Foundations (container 2)'){
                            steps {
                                container("python3-2") {
                                    ws("${WORKSPACE}/testing") {
                                        sh 'python -m pip install -U foundations-scheduler'
                                        sh 'python -m pip install ../dist/*.whl'
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Install Foundations (container 3)') {
                    stages{
                        stage('Install Foundations (container 3)'){
                            steps {
                                container("python3-3") {
                                    ws("${WORKSPACE}/testing") {
                                        sh 'python -m pip install ../dist/*.whl'
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Install Foundations (container 4)') {
                    stages{
                        stage('Install Foundations (container 4)'){
                            steps {
                                container("python3-4") {
                                    ws("${WORKSPACE}/testing") {
                                        sh 'python -m pip install ../dist/*.whl'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        stage('Python3 All Foundations Acceptance Tests'){
            failFast true
            parallel{
                stage('Parallel Foundations Acceptance Tests') {
                    stages {
                        stage('Python3 Foundations Acceptance Tests'){
                            steps{
                                container("python3") {
                                    ws("${WORKSPACE}/testing") {
                                        sh 'cp -r ../testing/* . || true'
                                        sh "python -Wi -m unittest -f -v acceptance"
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Parallel Foundations Acceptance Tests for Stageless Deploys') {
                    stages{
                        stage('Parallel Foundations Acceptance Tests for Stageless Deploys'){
                            steps {
                                container("python3-1") {
                                    ws("${WORKSPACE}/testing") {
                                        sh 'cp -r ../testing/* . || true'
                                        sh 'python -Wi -m unittest -f -v stageless_acceptance'
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Parallel Foundations Scheduler Acceptance Tests for Remote Deploys') {
                    stages{
                        stage('Python3 Foundations Scheduler Acceptance Tests for Remote Deploys') {
                            steps {
                                container("python3-2") {
                                    ws("${WORKSPACE}/testing") {
                                        sh 'cp -r ../testing/* . || true'
                                        sh 'export FOUNDATIONS_SCHEDULER_HOST=$FOUNDATIONS_SCHEDULER_ACCEPTANCE_HOST && python -Wi -m unittest -f -v scheduler_acceptance'
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Parallel Foundations REST API Acceptance Tests') {
                    stages{
                        stage('Python3 Foundations REST API Acceptance Tests') {
                            steps {
                                container("python3-3") {
                                    ws("${WORKSPACE}/foundations_rest_api/src") {
                                        sh "python -Wi -m unittest -f -v acceptance"
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Parallel Foundations Orbit Acceptance Tests') {
                    stages{
                        stage('Python3 Foundations Orbit Acceptance Tests') {
                            steps {
                                container("python3-4") {
                                    ws("${WORKSPACE}/testing") {
                                        sh 'cp -r ../testing/* . || true'
                                        sh 'export FOUNDATIONS_SCHEDULER_HOST=$FOUNDATIONS_SCHEDULER_ACCEPTANCE_HOST && python -Wi -m unittest -f -v orbit_acceptance'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
         stage('Install dependencies for Foundations UI (Atlas)') {
            steps {
                container("yarn") {
                    ws("${WORKSPACE}/foundations_ui/") {
                        sh "yarn install"
                    }
                }
            }
        }
        stage('Run Front End Unit Tests (Atlas)') {
            steps {
                container("yarn") {
                    ws("${WORKSPACE}/foundations_ui/") {
                        sh "yarn run test"
                    }
                }
            }
        }
        stage('Check for linting (Atlas)') {
            steps {
                container("yarn") {
                    ws("${WORKSPACE}/foundations_ui/") {
                        sh "node_modules/.bin/eslint ."
                    }
                }
            }
        }
        stage('Install dependencies for Foundations UI (Orbit)') {
            steps {
                container("yarn") {
                    ws("${WORKSPACE}/foundations_ui_orbit/") {
                        sh "yarn install"
                    }
                }
            }
        }
        stage('Check for linting (Orbit)') {
            steps {
                container("yarn") {
                    ws("${WORKSPACE}/foundations_ui_orbit/") {
                        sh "node_modules/.bin/eslint ."
                    }
                }
            }
        }
        stage('Upload Wheels to Releases') {
            steps {
                container("python3"){
                    sh "./upload_modules_to_artifactory.sh $NEXUS_PYPI"
                }
            }
        }
        stage('Build GUI and Rest API Images'){
            steps {
                container("python3"){
                    sh "./build_gui.sh"
                }
            }
        }
        stage('Push GUI and Rest API Images'){
            steps {
                container("python3"){
                    sh "./push_gui_images.sh"
                }
            }
        }
        stage('Push Model Package Images') {
            steps {
                container("python3"){
                    ws("${WORKSPACE}/foundations_model_package/src"){
                        sh './push_green_images.sh'
                    }
                }
            }
        }
        stage("Calculate Recovery Metrics") {
            steps {
                script {
                    def last_build = currentBuild.getPreviousBuild()
                    def last_failed_build
                    def current_time = System.currentTimeMillis()
                    
                    while(last_build != null && last_build.result == "FAILURE") {
                        last_failed_build = last_build
                        last_build = last_build.getPreviousBuild()
                    }
                    
                    if(last_failed_build != null) {
                        time_to_recovery = current_time - last_failed_build.getTimeInMillis() 
                        customMetrics["time_to_recovery"] = time_to_recovery
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                customMetricsMap["jenkins_data"] = customMetrics
            }
            influxDbPublisher selectedTarget: 'foundations', customPrefix: 'foundations', customProjectName: 'foundations', jenkinsEnvParameterField: '', jenkinsEnvParameterTag: '', customDataMap: customMetricsMap
        }
        failure {
            script {
                def output_logs = String.join('\n', currentBuild.rawBuild.getLog(200))
                def attachments = [
                    [
                        pretext: '@channel Build failed for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.',
                        text: output_logs,
                        fallback: '@channel Build failed for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.',
                        color: '#FF0000'
                    ]
                ]

                slackSend(channel: '#f9s-builds', attachments: attachments)
            }
        }
        success {
            slackSend color: '#00FF00', message: 'Build succeeded for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.'
        }
    }
}