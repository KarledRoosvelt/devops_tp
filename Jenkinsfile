pipeline {
    agent any

    environment {
        IMAGE_NAME      = "sum-python-app"
        CONTAINER_NAME  = "sum_container_${BUILD_NUMBER}"
        TEST_FILE_PATH  = "test_variables.txt"
        DOCKERHUB_IMAGE = "karledroosvelt/sum-python-app"
    }

    stages {

        stage('Build') {
            steps {
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Run') {
            steps {
                bat "docker run -d --name %CONTAINER_NAME% %IMAGE_NAME%"
            }
        }

        stage('Test') {
            steps {
                script {
                    def testLines = readFile(TEST_FILE_PATH)
                        .split('\\r?\\n')
                        .findAll { it.trim() }

                    for (line in testLines) {
                        def parts = line.trim().split('\\s+')

                        if (parts.size() < 3) {
                            error "Ligne de test invalide : ${line}"
                        }

                        def a        = parts[0]
                        def b        = parts[1]
                        def expected = parts[2].toDouble()

                        def output = bat(
                            script: "docker exec %CONTAINER_NAME% python /app/sum.py ${a} ${b}",
                            returnStdout: true
                        ).trim()

                        def result = output.split('\\r?\\n')[-1].trim().toDouble()

                        // Comparaison avec tolérance (problème 1.1 + 2.2)
                        if (Math.abs(result - expected) < 0.0001) {
                            echo "OK: ${a} + ${b} = ${result}"
                        } else {
                            error "FAILED: ${a} + ${b} => obtenu ${result}, attendu ${expected}"
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_PASS'
                )]) {
                    bat """
                        echo %DOCKERHUB_PASS% | docker login -u %DOCKERHUB_USER% --password-stdin
                        docker tag %IMAGE_NAME% %DOCKERHUB_IMAGE%:latest
                        docker push %DOCKERHUB_IMAGE%:latest
                    """
                }
            }
        }
    }

    post {
        always {
            bat "docker rm -f %CONTAINER_NAME%"
        }
    }
}
