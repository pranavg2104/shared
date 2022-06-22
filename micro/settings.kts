import jetbrains.buildServer.configs.kotlin.v2019_2.*
import jetbrains.buildServer.configs.kotlin.v2019_2.buildSteps.python
import jetbrains.buildServer.configs.kotlin.v2019_2.triggers.finishBuildTrigger
import jetbrains.buildServer.configs.kotlin.v2019_2.triggers.vcs
import jetbrains.buildServer.configs.kotlin.v2019_2.vcs.GitVcsRoot

/*
The settings script is an entry point for defining a TeamCity
project hierarchy. The script should contain a single call to the
project() function with a Project instance or an init function as
an argument.

VcsRoots, BuildTypes, Templates, and subprojects can be
registered inside the project using the vcsRoot(), buildType(),
template(), and subProject() methods respectively.

To debug settings scripts in command-line, run the

    mvnDebug org.jetbrains.teamcity:teamcity-configs-maven-plugin:generate

command and attach your debugger to the port 8000.

To debug in IntelliJ Idea, open the 'Maven Projects' tool window (View
-> Tool Windows -> Maven Projects), find the generate task node
(Plugins -> teamcity-configs -> teamcity-configs:generate), the
'Debug' option is available in the context menu for the task.
*/

version = "2021.2"

project {

    vcsRoot(HttpsGitlabKpitComPranavg2demoConanGitRefsHeadsTeamcity)

    buildType(Mgm002postBuild)
    buildType(MGM001)
    buildType(MGM002)
    buildType(Test)
    buildType(Mgm001postBuild)

    params {
        param("feature2", "CRUZ_CONTROL")
        password("pass", "credentialsJSON:ea446cbe-a0f2-43a2-aea5-799a7f747681", display = ParameterDisplay.HIDDEN)
        password("securepass", "credentialsJSON:65469971-4541-4721-9831-0232e8dd7950", display = ParameterDisplay.HIDDEN)
        text("user", "admin", display = ParameterDisplay.HIDDEN, allowEmpty = false)
        param("feature1", "TURN_INDICATOR")
    }
}

object MGM001 : BuildType({
    name = "MGM001"

    vcs {
        root(DslContext.settingsRoot)
    }

    steps {
        python {
            name = "Build"
            command = script {
                content = """print("Hello")"""
            }
        }
        python {
            name = "Build"
            command = script {
                content = """print("Hello Gitanjali")"""
            }
        }
    }

    triggers {
        vcs {
            branchFilter = "+:<default>"
        }
    }
})

object MGM002 : BuildType({
    name = "MGM002"

    vcs {
        root(DslContext.settingsRoot)
    }

    steps {
        python {
            workingDir = "resources"
            command = script {
                content = """
                    import time
                    
                    print("Start")
                    time.sleep(40)
                    print("End")
                """.trimIndent()
            }
        }
    }
})

object Mgm001postBuild : BuildType({
    name = "MGM001_POST_BUILD"

    params {
        param("pipeline", "VECU_CREATION_FROM_VVT")
    }

    vcs {
        root(HttpsGitlabKpitComPranavg2demoConanGitRefsHeadsTeamcity)
    }

    steps {
        python {
            command = custom {
                arguments = "producer.py ${MGM001.depParamRefs["system.teamcity.buildType.id"]} %feature1% %user% %pass% %pipeline%"
            }
        }
    }

    triggers {
        finishBuildTrigger {
            buildType = "${MGM001.id}"
        }
    }

    dependencies {
        snapshot(MGM001) {
            runOnSameAgent = true
            reuseBuilds = ReuseBuilds.NO
            onDependencyFailure = FailureAction.IGNORE
            onDependencyCancel = FailureAction.ADD_PROBLEM
        }
    }
})

object Mgm002postBuild : BuildType({
    name = "MGM002_POST_BUILD"

    params {
        param("pipeline", "AUTOMATION_OF_.SIC_FILE")
    }

    vcs {
        root(HttpsGitlabKpitComPranavg2demoConanGitRefsHeadsTeamcity)
    }

    steps {
        python {
            command = custom {
                arguments = "producer.py ${MGM002.depParamRefs["system.teamcity.buildType.id"]} %feature2% %user% %pass% %pipeline%"
            }
        }
    }

    triggers {
        finishBuildTrigger {
            buildType = "${MGM002.id}"
        }
    }

    dependencies {
        snapshot(MGM002) {
            runOnSameAgent = true
            reuseBuilds = ReuseBuilds.NO
            onDependencyFailure = FailureAction.IGNORE
            onDependencyCancel = FailureAction.ADD_PROBLEM
        }
    }
})

object Test : BuildType({
    name = "TEST"

    steps {
        python {
            command = script {
                content = """print("%teamcity.serverUrl%")"""
            }
        }
    }
})

object HttpsGitlabKpitComPranavg2demoConanGitRefsHeadsTeamcity : GitVcsRoot({
    name = "https://gitlab.kpit.com/pranavg2/demo-conan.git#refs/heads/teamcity"
    url = "https://gitlab.kpit.com/pranavg2/demo-conan.git"
    branch = "refs/heads/teamcity"
    branchSpec = "refs/heads/*"
    authMethod = password {
        userName = "pranavg2"
        password = "credentialsJSON:6eebb1e9-85e2-4bca-8d98-6217b7aede13"
    }
})
