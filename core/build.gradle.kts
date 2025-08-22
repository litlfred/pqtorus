plugins {
    kotlin("multiplatform")
}

kotlin {
    wasmJs {
        browser {
            testTask {
                useKarma {
                    useFirefoxHeadless()
                }
            }
        }
        binaries.executable()
    }
    
    sourceSets {
        val commonMain by getting {
            dependencies {
            }
        }
        
        val commonTest by getting {
            dependencies {
                implementation(kotlin("test"))
            }
        }
        
        val wasmJsMain by getting {
            dependencies {
            }
        }
    }
}