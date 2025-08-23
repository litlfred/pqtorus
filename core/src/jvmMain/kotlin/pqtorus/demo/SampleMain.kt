package pqtorus.demo

import org.hipparchus.complex.Complex as HipparchusComplex
import pqtorus.render.*
import pqtorus.math.Weierstrass
import java.io.File

/**
 * Sample CLI application demonstrating the Hipparchus-based Weierstrass embedding.
 * Generates sample grids and exports to OBJ/PLY/CSV formats.
 */
object SampleMain {
    
    @JvmStatic
    fun main(args: Array<String>) {
        println("PQTorus Hipparchus-based Weierstrass Embedding Demo")
        println("==================================================")
        
        // Default parameters
        val p = 2.0
        val q = 3.0
        val gridSize = 20
        
        println("Lattice parameters: p = $p, q = $q")
        println("Grid size: ${gridSize}x$gridSize")
        println()
        
        // Test basic mathematical functions
        println("Testing mathematical functions...")
        testMathematicalFunctions(p, q)
        println()
        
        // Generate embedded torus
        println("Generating embedded torus...")
        val torus = generateEmbeddedTorus(p, q, gridSize)
        println("Generated ${torus.vertices.size} vertices and ${torus.faces.size} faces")
        println()
        
        // Export to different formats
        val outputDir = "output"
        File(outputDir).mkdirs()
        
        println("Exporting to files...")
        
        // Export OBJ
        val objFile = File("$outputDir/torus_p${p}_q${q}.obj")
        objFile.writeText(torus.toOBJ())
        println("Exported OBJ: ${objFile.absolutePath}")
        
        // Export PLY
        val plyFile = File("$outputDir/torus_p${p}_q${q}.ply")
        plyFile.writeText(torus.toPLY())
        println("Exported PLY: ${plyFile.absolutePath}")
        
        // Export CSV
        val csvFile = File("$outputDir/torus_p${p}_q${q}.csv")
        csvFile.writeText(torus.toCSV())
        println("Exported CSV: ${csvFile.absolutePath}")
        
        println()
        println("Demo completed successfully!")
    }
    
    /**
     * Test basic mathematical functions and validate results.
     */
    private fun testMathematicalFunctions(p: Double, q: Double) {
        // Test point
        val z = HipparchusComplex(p / 4.0, q / 4.0)
        
        // Compute Weierstrass functions
        val wp = Weierstrass.wp(z, p, q)
        val wpPrime = Weierstrass.wpPrime(z, p, q)
        
        println("At z = $z:")
        println("  ℘(z) = $wp")
        println("  ℘'(z) = $wpPrime")
        
        // Verify differential equation: (℘')² = 4℘³ - g₂℘ - g₃
        val verification = Weierstrass.verifyDifferentialEquation(z, p, q)
        println("  Differential equation verification: |error| = ${verification.abs()}")
        
        if (verification.abs() < 1e-10) {
            println("  ✓ Differential equation satisfied")
        } else {
            println("  ⚠ Differential equation error larger than expected")
        }
        
        // Test lattice invariants
        val g2 = Weierstrass.g2(p, q)
        val g3 = Weierstrass.g3(p, q)
        println("  g₂ = $g2")
        println("  g₃ = $g3")
        
        // Test special case: for square lattice (τ = i), g₃ should be 0
        if (kotlin.math.abs(p - q) < 1e-10) {
            println("  Square lattice: g₃ should be ≈ 0, actual: $g3")
        }
    }
    
    /**
     * Generate sample with custom parameters from command line arguments.
     */
    fun generateCustomSample(args: Array<String>) {
        if (args.size < 2) {
            println("Usage: SampleMain <p> <q> [gridSize] [outputPrefix]")
            return
        }
        
        val p = args[0].toDoubleOrNull() ?: run {
            println("Invalid p parameter: ${args[0]}")
            return
        }
        
        val q = args[1].toDoubleOrNull() ?: run {
            println("Invalid q parameter: ${args[1]}")
            return
        }
        
        val gridSize = if (args.size > 2) {
            args[2].toIntOrNull() ?: 20
        } else 20
        
        val outputPrefix = if (args.size > 3) args[3] else "torus"
        
        println("Generating torus with p=$p, q=$q, gridSize=$gridSize")
        
        val torus = generateEmbeddedTorus(p, q, gridSize)
        
        // Export files
        val outputDir = "output"
        File(outputDir).mkdirs()
        
        File("$outputDir/${outputPrefix}_p${p}_q${q}.obj").writeText(torus.toOBJ())
        File("$outputDir/${outputPrefix}_p${p}_q${q}.ply").writeText(torus.toPLY())
        File("$outputDir/${outputPrefix}_p${p}_q${q}.csv").writeText(torus.toCSV())
        
        println("Exported to $outputDir/")
    }
}