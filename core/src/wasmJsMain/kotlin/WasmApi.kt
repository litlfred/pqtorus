package com.pqtorus.core

private val torusGenerator = TorusGenerator()

/**
 * Generate torus geometry and return as JSON string
 */
@JsExport
fun generateTorusJson(p: Double, q: Double, degree: Int, meshDensity: Int = 20): String {
    val geometry = torusGenerator.generateTorus(p, q, degree, meshDensity)
    
    // Manual JSON serialization since kotlinx.serialization doesn't support Wasm yet
    val verticesJson = geometry.vertices.joinToString(",") { vertex ->
        "{\"x\":${vertex.x},\"y\":${vertex.y},\"z\":${vertex.z}}"
    }
    
    val facetsJson = geometry.facets.joinToString(",") { facet ->
        "{\"v1\":${facet.v1},\"v2\":${facet.v2},\"v3\":${facet.v3},\"v4\":${facet.v4}}"
    }
    
    return """
        {
            "vertices":[$verticesJson],
            "facets":[$facetsJson],
            "jInvariant":{"real":${geometry.jInvariant.real},"imag":${geometry.jInvariant.imag}},
            "discriminant":{"real":${geometry.discriminant.real},"imag":${geometry.discriminant.imag}},
            "tau":{"real":${geometry.tau.real},"imag":${geometry.tau.imag}}
        }
    """.trimIndent()
}

/**
 * Check if a number is prime
 */
@JsExport
fun checkIsPrime(n: Int): Boolean {
    return isPrime(n)
}

/**
 * Get next prime number
 */
@JsExport
fun getNextPrime(n: Int): Int {
    return nextPrime(n)
}

/**
 * Get library version info
 */
@JsExport
fun getVersion(): String {
    return "1.0.0"
}