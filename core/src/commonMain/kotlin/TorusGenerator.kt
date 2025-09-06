package com.pqtorus.core

import kotlin.math.*

/**
 * Core class for generating elliptic curve tori visualization
 */
class TorusGenerator {
    
    /**
     * Generate torus geometry for given parameters
     * 
     * Creates elliptic curve torus visualization for lattice ℂ/L where:
     * L = {n₁p + n₂qi | n₁,n₂ ∈ ℤ} with prime periods p,q
     * 
     * Mathematical formulas:
     * - Lattice periods: ω₁ = p + 0i, ω₂ = 0 + qi
     * - Tau: τ = ω₂/ω₁ = qi/p = i(q/p)  
     * - Degree-d scaling: L_d = L/2^d
     * - J-invariant: 1728 (placeholder for j(τ))
     * - Discriminant: p*qi (simplified form)
     * 
     * @param p First prime period (real)
     * @param q Second prime period (real)  
     * @param degree Degree of approximation (d >= 0)
     * @param meshDensity Number of subdivisions for the mesh
     * @return TorusGeometry containing vertices, facets, and invariants
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
        
        // Generate lattice points for degree d approximation
        val latticePoints = generateLatticePoints(period1, period2, degree)
        
        // Project to torus surface and create 3D vertices
        val vertices = projectToTorus(latticePoints, period1, period2, meshDensity)
        
        // Generate facets (quadrilaterals)
        val facets = generateFacets(meshDensity)
        
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
    
    /**
     * Generate lattice points for degree d approximation
     * 
     * Formula: L_d = {(n₁ω₁ + n₂ω₂)/2^d | n₁,n₂ ∈ ℤ}
     * Where ω₁ = p, ω₂ = qi, and scale = 2^(-d)
     * 
     * @param period1 First lattice period (p + 0i)
     * @param period2 Second lattice period (0 + qi)
     * @param degree Approximation degree d ≥ 0
     * @return List of complex lattice points
     */
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
    
    /**
     * Project lattice points to 3D torus surface
     * 
     * Current implementation uses standard geometric torus:
     * x(u,v) = (R + r*cos(v)) * cos(u)
     * y(u,v) = (R + r*cos(v)) * sin(u)  
     * z(u,v) = r * sin(v)
     * 
     * Where R = 2.0 (major radius), r = 0.5 (minor radius)
     * u,v ∈ [0,2π] parametrize the surface
     * 
     * Note: Actual lattice points not used in current projection.
     * Proper elliptic torus would use Weierstrass ℘-function.
     * 
     * @param latticePoints Generated lattice points (unused in current implementation)
     * @param period1 First lattice period
     * @param period2 Second lattice period  
     * @param meshDensity Grid resolution for torus mesh
     * @return List of 3D vertices
     */
        latticePoints: List<Complex>, 
        period1: Complex, 
        period2: Complex,
        meshDensity: Int
    ): List<Vertex3D> {
        val vertices = mutableListOf<Vertex3D>()
        
        // Create a regular torus parametrization
        val majorRadius = 2.0
        val minorRadius = 0.5
        
        for (i in 0 until meshDensity) {
            for (j in 0 until meshDensity) {
                val u = 2 * PI * i / meshDensity
                val v = 2 * PI * j / meshDensity
                
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
    
    /**
     * Calculate elliptic curve invariants
     * 
     * Mathematical formulas for lattice with periods ω₁ = p, ω₂ = qi:
     * - Tau: τ = ω₂/ω₁ = qi/p = i(q/p)
     * - J-invariant: j(τ) = 1728*g₂³/(g₂³-27g₃²) [currently placeholder: 1728]
     * - Discriminant: Δ = Im(ω̄₁ω₂) = pq [currently simplified as p*qi]
     * 
     * Current implementation uses simplified calculations.
     * See MATHEMATICAL_FORMULAS.md for proper elliptic function theory.
     * 
     * @param period1 First lattice period (p + 0i)
     * @param period2 Second lattice period (0 + qi)
     * @return EllipticInvariants containing j-invariant and discriminant
     */
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