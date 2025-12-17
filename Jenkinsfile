pipeline {
    // Indique que le pipeline peut s’exécuter sur n’importe quel agent Jenkins
    agent any

    environment {
        // Variable pour stocker l’ID du conteneur Docker
        CONTAINER_ID = ""

        // Chemin du projet (Dockerfile)
        DIR_PATH = "."

        // Fichier contenant les variables de test
        TEST_FILE_PATH = "test_variables.txt"

        // Nom de l’image Docker
        IMAGE_NAME = "sum-python-app"

        // Nom de l’image sur DockerHub
        DOCKERHUB_IMAGE = "yourdockerhub/sum-python-app"
    }

    stages {

        stage('Build') {
            steps {
                // Construction de l’image Docker
                bat "docker build -t %IMAGE_NAME% %DIR_PATH%"
            }
        }

        stage('Run') {
            steps {
                script {
                    // Démarre le conteneur en mode détaché (-d)
                    // returnStdout permet de récupérer l’ID du conteneur
                    def output = bat(
                        script: "docker run -d %IMAGE_NAME%",
                        returnStdout: true
                    )

                    // Récupération de l’ID du conteneur
                    def lines = output.split('\n')
                    CONTAINER_ID = lines[lines.length - 1].trim()
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Lecture du fichier de test
                    def testLines = readFile(TEST_FILE_PATH).split('\n')

                    // Boucle sur chaque ligne de test
                    for (line in testLines) {

                        // Séparation des valeurs : arg1, arg2, somme attendue
                        def vars = line.split(' ')
                        def arg1 = vars[0]
                        def arg2 = vars[1]
                        def expectedSum = vars[2].toFloat()

                        // Exécution du script sum.py dans le conteneur
                        def output = bat(
                            script: "docker exec ${CONTAINER_ID} python /app/sum.py ${arg1} ${arg2}",
                            returnStdout: true
                        )

                        // Récupération du résultat retourné par le script
                        def result = output.split('\n')[-1].trim().toFloat()

                        // Comparaison du résultat avec la valeur attendue
                        if (result == expectedSum) {
                            echo "Test OK : ${arg1} + ${arg2} = ${result}"
                        } else {
                            error "Test FAILED : attendu ${expectedSum}, obtenu ${result}"
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                // Connexion à DockerHub
                bat "docker login"

                // Tag de l’image avant publication
                bat "docker tag %IMAGE_NAME% %DOCKERHUB_IMAGE%"

                // Push de l’image vers DockerHub
                bat "docker push %DOCKERHUB_IMAGE%"
            }
        }
    }

    post {
        always {
            // Arrêt du conteneur même si le pipeline échoue
            bat "docker stop %CONTAINER_ID%"

            // Suppression du conteneur pour éviter l’encombrement
            bat "docker rm %CONTAINER_ID%"
        }
    }
}
