import libs.jenkins.TelegramMessage

String TG_CHAT_ID = "ID"
String TG_BOT_ID  = "ID"
String TG_MESSAGE
boolean ALLURE_OK = true
String logs

node('selenium0'){

    properties(
       [
           pipelineTriggers([cron('0 9 * * *')]),
       ]
    )

    stage('SCM to build') {
        cleanWs()
        git credentialsId: 'jenkins_bb',
                url: 'git@bitbucket.org:path_name.git',
                branch: 'master'
    }

    stage('Install dependencies')
        {
            sh '''
                pip3 install --upgrade pip
                pip3 install -r ./requirements.txt
            '''
        }

    stage('Run Selenium tests')
        {
            try {
                sh """
                    #!/bin/bash
                    python3 -m pytest --no-header ./test_Test_Examples.py --alluredir=allure-result
                    """

            } catch(Exception e) {
                ALLURE_OK = false
            }

            stage('Create final logfile'){
                    sh 'cat *.txt > result_log.txt'
            }
        }


    allure([
            includeProperties: false,
            reportBuildPolicy: 'ALWAYS',
            results: [[path: 'allure-result']]
    ])

    logs = readFile './result_log.txt'

    if(ALLURE_OK)
    {
                TG_MESSAGE = """Success log\nAllure Detail: ${BUILD_URL}/allure"""

            } else {

                if(logs.length() < 0){
                    logs.delete()
                }

                TG_MESSAGE = """Fail:\n${logs}\n Allure Detail: ${BUILD_URL}/allure"""

            }


    new TelegramMessage(
        message: TG_MESSAGE,
        chatId: TG_CHAT_ID,
        botId: TG_BOT_ID).send()

}
