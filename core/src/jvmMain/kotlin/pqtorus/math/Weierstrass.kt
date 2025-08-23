package pqtorus.math

import org.hipparchus.complex.Complex as HipparchusComplex
import kotlin.math.*

/**
 * Weierstrass elliptic function implementation using the Jacobi route with theta constants.
 * Implements ℘(z; L) and ℘′(z; L) for rectangular lattice L = Z·p + Z·(q·i).
 */
object Weierstrass {
    
    /**
     * Data class to hold lattice invariants computed from theta constants.
     */
    data class LatticeInvariants(
        val e1: Double,
        val e2: Double, 
        val e3: Double,
        val m: Double,
        val scale: Double,
        val g2: Double,
        val g3: Double
    )
    
    /**
     * Compute lattice invariants from theta constants for τ = i·(q/p).
     * Uses the formulas:
     * scale = π / (2p)
     * e1 = scale² * (θ₃⁴ + θ₄⁴) / 3
     * e2 = scale² * (θ₂⁴ - θ₄⁴) / 3  
     * e3 = -e1 - e2
     * m = (e2 - e3) / (e1 - e3)
     */
    fun computeInvariants(p: Double, q: Double): LatticeInvariants {
        val (theta2, theta3, theta4) = Theta.thetaConstants(p, q)
        
        val scale = PI / (2.0 * p)
        val scale2 = scale * scale
        
        // Compute theta constants to fourth power
        val theta2_4 = theta2.pow(4.0).real
        val theta3_4 = theta3.pow(4.0).real
        val theta4_4 = theta4.pow(4.0).real
        
        // Compute e-invariants
        val e1 = scale2 * (theta3_4 + theta4_4) / 3.0
        val e2 = scale2 * (theta2_4 - theta4_4) / 3.0
        val e3 = -e1 - e2
        
        // Compute Jacobi parameter m = k²
        val m = (e2 - e3) / (e1 - e3)
        
        // Compute g2 and g3 invariants
        val g2 = 4.0 * (e1 * e2 + e2 * e3 + e3 * e1)
        val g3 = 4.0 * e1 * e2 * e3
        
        return LatticeInvariants(e1, e2, e3, m, scale, g2, g3)
    }
    
    /**
     * Weierstrass ℘(z; L) function using Jacobi elliptic functions.
     * Formula: ℘(z) = e3 + (e1 - e3) / sn²(U|m)
     * where U = √(e1 - e3) * z
     */
    fun wp(z: HipparchusComplex, p: Double, q: Double): HipparchusComplex {
        val invariants = computeInvariants(p, q)
        
        // Compute U = √(e1 - e3) * z
        val sqrtE1MinusE3 = sqrt(invariants.e1 - invariants.e3)
        val U = z.multiply(sqrtE1MinusE3)
        
        // Compute sn(U|m) with pole protection
        val sn = Jacobi.snSafe(U, invariants.m)
        val sn2 = sn.multiply(sn)
        
        // ℘(z) = e3 + (e1 - e3) / sn²(U|m)
        val e1MinusE3 = invariants.e1 - invariants.e3
        return HipparchusComplex(invariants.e3, 0.0).add(HipparchusComplex(e1MinusE3, 0.0).divide(sn2))
    }
    
    /**
     * Weierstrass ℘′(z; L) derivative function using Jacobi elliptic functions.
     * Formula: ℘′(z) = -2 * (e1 - e3)^(3/2) * cn(U|m) * dn(U|m) / sn³(U|m)
     * where U = √(e1 - e3) * z
     */
    fun wpPrime(z: HipparchusComplex, p: Double, q: Double): HipparchusComplex {
        val invariants = computeInvariants(p, q)
        
        // Compute U = √(e1 - e3) * z
        val sqrtE1MinusE3 = sqrt(invariants.e1 - invariants.e3)
        val U = z.multiply(sqrtE1MinusE3)
        
        // Compute Jacobi functions
        val (sn, cn, dn) = Jacobi.jacobiHipparchusComplex(U, invariants.m)
        
        // Handle pole case
        val sn3 = if (sn.abs() < 1e-12) {
            // Apply small perturbation to avoid pole
            val perturbedU = U.add(HipparchusComplex(1e-12, 1e-12))
            val (snPerturbed, _, _) = Jacobi.jacobiHipparchusComplex(perturbedU, invariants.m)
            snPerturbed.pow(3.0)
        } else {
            sn.pow(3.0)
        }
        
        // ℘′(z) = -2 * (e1 - e3)^(3/2) * cn(U|m) * dn(U|m) / sn³(U|m)
        val e1MinusE3_3_2 = (invariants.e1 - invariants.e3).pow(1.5)
        val numerator = cn.multiply(dn).multiply(HipparchusComplex(-2.0 * e1MinusE3_3_2, 0.0))
        
        return numerator.divide(sn3)
    }
    
    /**
     * Compute g2 invariant from lattice parameters.
     * Can be used for validation: (℘′)² = 4℘³ - g2℘ - g3
     */
    fun g2(p: Double, q: Double): Double {
        return computeInvariants(p, q).g2
    }
    
    /**
     * Compute g3 invariant from lattice parameters.
     */
    fun g3(p: Double, q: Double): Double {
        return computeInvariants(p, q).g3
    }
    
    /**
     * Verify the Weierstrass differential equation at a point z.
     * Returns (℘′(z))² - 4(℘(z))³ + g2·℘(z) + g3
     * Should be close to zero for correct implementation.
     */
    fun verifyDifferentialEquation(z: HipparchusComplex, p: Double, q: Double): HipparchusComplex {
        val wp = wp(z, p, q)
        val wpPrime = wpPrime(z, p, q)
        val invariants = computeInvariants(p, q)
        
        val lhs = wpPrime.multiply(wpPrime)
        val rhs = wp.pow(3.0).multiply(4.0)
            .subtract(wp.multiply(invariants.g2))
            .subtract(HipparchusComplex(invariants.g3, 0.0))
        
        return lhs.subtract(rhs)
    }
}