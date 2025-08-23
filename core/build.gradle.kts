plugins {
    kotlin("multiplatform")
}

kotlin {
    jvm {
        jvmToolchain(17)
    }
    
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
        
        val jvmMain by getting {
            dependencies {
                implementation("org.hipparchus:hipparchus-core:4.0.1")
            }
        }
        
        val jvmTest by getting {
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