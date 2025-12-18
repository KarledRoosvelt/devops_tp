pipeline {
    agent any

    environment {
        IMAGE_NAME      = "sum-python-app"
        CONTAINER_NAME  = "sum_container_${BUILD_NUMBER}"   // nom unique à chaque build
        TEST_FILE_PATH  = "test_variables.txt"
        DOCKERHUB_IMAGE = "karledroosvelt/sum-python-app"    // image docker
    }

    stages {
        stage('Build') {
            steps {
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Run') {
            steps {
                // Lance le conteneur en arrière-plan avec un nom connu
                bat "docker run -d --name %CONTAINER_NAME% %IMAGE_NAME%"
            }
        }

        stage('Test') {
            steps {
                script {
                    // Lit le fichier et enlève les lignes vides
                    def testLines = readFile(env.TEST_FILE_PATH)
                        .split('\\r?\\n')
                        .findAll { it?.trim() }

                    for (line in testLines) {
                        // Découpe en gérant plusieurs espaces
                        def parts = line.trim().split('\\s+')

                        // Sécurité si une ligne est mal formée
                        if (parts.size() < 3) {
                            error "Ligne de test invalide: '${line}' (attendu: a b somme)"
                        }

                        def a = parts[0]
                        def b = parts[1]
                        def expected = parts[2].toDouble()

                        // Exécute sum.py dans le conteneur
                        def out = bat(
                            script: "docker exec %CONTAINER_NAME% python /app/sum.py ${a} ${b}",
                            returnStdout: true
                        ).trim()

                        // Le résultat est la dernière ligne utile
                        def result = out.split('\\r?\\n')[-1].trim().toDouble()

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
        post {
        always {
            // Nettoyage: stop + rm même si Test échoue
            bat "docker rm -f %CONTAINER_NAME%"
        }
    }
}
}