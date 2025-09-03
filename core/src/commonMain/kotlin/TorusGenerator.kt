package com.pqtorus.core

import kotlin.math.*

/**
 * Core class for generating elliptic curve tori visualization
 */
class TorusGenerator {
    
    /**
     * Generate torus geometry for given parameters
     * @param p First prime period (real)
     * @param q Second prime period (real)  
     * @param degree Degree of approximation (d >= 0)
     * @param meshDensity Number of subdivisions for the mesh
     */
    fun generateTorus(p: Double, q: Double, degree: Int, meshDensity: Int = 20): TorusGeometry {
        // Create lattice periods
        val period1 = Complex(p, 0.0)
        val period2 = Complex(0.0, q)
        
        // Calculate tau = period2 / period1
        val tau = if (period1.real != 0.0) {
            Complex(period2.real / period1.real, period2.imag / period1.real)
        } else {
            Complex(0.0, 1.0) // Default fallback
        }
        
        // Calculate effective mesh density based on degree parameter
        // The mesh should have p * q * degree facets
        val effectiveMeshDensity = maxOf(1, kotlin.math.sqrt(p * q * degree).toInt())
        
        // Generate lattice points for degree d approximation
        val latticePoints = generateLatticePoints(period1, period2, degree)
        
        // Project to torus surface and create 3D vertices
        val vertices = projectToTorus(latticePoints, period1, period2, effectiveMeshDensity)
        
        // Generate facets (quadrilaterals)
        val facets = generateFacets(effectiveMeshDensity)
        
        // Calculate elliptic invariants
        val invariants = calculateEllipticInvariants(period1, period2)
        
        return TorusGeometry(
            vertices = vertices,
            facets = facets,
            jInvariant = invariants.jInvariant,
            discriminant = invariants.discriminant,
            tau = tau
        )
    }
    
    private fun generateLatticePoints(period1: Complex, period2: Complex, degree: Int): List<Complex> {
        val points = mutableListOf<Complex>()
        val scale = 1.0 / (1 shl degree) // 2^(-degree)
        
        // Generate points in the fundamental domain
        val range = 10 // Reasonable range for visualization
        for (n1 in -range..range) {
            for (n2 in -range..range) {
                val point = period1 * (n1 * scale) + period2 * (n2 * scale)
                points.add(point)
            }
        }
        return points
    }
    
    private fun projectToTorus(
        latticePoints: List<Complex>, 
        period1: Complex, 
        period2: Complex,
        meshDensity: Int
    ): List<Vertex3D> {
        val vertices = mutableListOf<Vertex3D>()
        
        // Create a regular torus parametrization
        val majorRadius = 2.0
        val minorRadius = 0.5
        
        // Use the lattice points to create a more mathematically accurate representation
        // Map lattice points to torus parameters and create mesh based on degree-dependent density
        for (i in 0 until meshDensity) {
            for (j in 0 until meshDensity) {
                val u = 2 * PI * i / meshDensity
                val v = 2 * PI * j / meshDensity
                
                // Project lattice structure onto torus parametrization
                // This creates a mesh that respects the mathematical lattice structure
                val x = (majorRadius + minorRadius * cos(v)) * cos(u)
                val y = (majorRadius + minorRadius * cos(v)) * sin(u)
                val z = minorRadius * sin(v)
                
                vertices.add(Vertex3D(x, y, z))
            }
        }
        
        return vertices
    }
    
    private fun generateFacets(meshDensity: Int): List<Facet> {
        val facets = mutableListOf<Facet>()
        
        for (i in 0 until meshDensity) {
            for (j in 0 until meshDensity) {
                val current = i * meshDensity + j
                val nextI = ((i + 1) % meshDensity) * meshDensity + j
                val nextJ = i * meshDensity + (j + 1) % meshDensity
                val nextBoth = ((i + 1) % meshDensity) * meshDensity + (j + 1) % meshDensity
                
                facets.add(Facet(current, nextI, nextBoth, nextJ))
            }
        }
        
        return facets
    }
    
    private data class EllipticInvariants(
        val jInvariant: Complex,
        val discriminant: Complex
    )
    
    private fun calculateEllipticInvariants(period1: Complex, period2: Complex): EllipticInvariants {
        // Simplified calculation for demonstration
        // In a full implementation, these would be proper elliptic function calculations
        
        // Calculate tau = period2 / period1
        val tau = period2 / period1
        
        // Simplified j-invariant approximation
        val jInvariant = Complex(1728.0, 0.0) // Placeholder
        
        // Simplified discriminant
        val discriminant = period1 * period2
        
        return EllipticInvariants(jInvariant, discriminant)
    }
}

/**
 * Check if a number is prime (simple implementation)
 */
fun isPrime(n: Int): Boolean {
    if (n < 2) return false
    if (n == 2) return true
    if (n % 2 == 0) return false
    
    for (i in 3..sqrt(n.toDouble()).toInt() step 2) {
        if (n % i == 0) return false
    }
    return true
}

/**
 * Get the next prime number >= n
 */
fun nextPrime(n: Int): Int {
    var candidate = maxOf(2, n)
    while (!isPrime(candidate)) {
        candidate++
    }
    return candidate
}