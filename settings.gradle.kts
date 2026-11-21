pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
        maven { url = uri("https://maven-central.storage-download.googleapis.com/maven2") }
        maven { url = uri("https://maven.google.com") }
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven { url = uri("https://maven-central.storage-download.googleapis.com/maven2") }
        maven { url = uri("https://maven.google.com") }
    }
}

rootProject.name = "OnePieceAIWorld"
include(":app")
