package pqtorus.math

import org.hipparchus.complex.Complex as HipparchusComplex
import kotlin.test.Test
import kotlin.test.assertTrue
import kotlin.math.*

/**
 * Unit tests for the Hipparchus-based Weierstrass elliptic function implementation.
 * Tests θ-constants, Jacobi identities, and Weierstrass differential equation.
 */
class WeierstrassTest {
    
    companion object {
        private const val TOLERANCE = 1e-10
    }
    
    @Test
    fun testThetaConstantsForSquareLattice() {
        // For square lattice τ = i, test known theta constant relationships
        val p = 1.0
        val q = 1.0  // τ = i
        
        val (theta2, theta3, theta4) = Theta.thetaConstants(p, q)
        
        // For τ = i, we have special relationships between theta constants
        // θ₃(0|i) and θ₄(0|i) should be real and positive
        assertTrue(abs(theta3.imaginary) < TOLERANCE, "θ₃(0|i) should be real")
        assertTrue(abs(theta4.imaginary) < TOLERANCE, "θ₄(0|i) should be real")
        assertTrue(theta3.real > 0, "θ₃(0|i) should be positive")
        assertTrue(theta4.real > 0, "θ₄(0|i) should be positive")
        
        // θ₂(0|i) should be real and positive
        assertTrue(abs(theta2.imaginary) < TOLERANCE, "θ₂(0|i) should be real")
        assertTrue(theta2.real > 0, "θ₂(0|i) should be positive")
        
        println("Square lattice theta constants:")
        println("  θ₂(0|i) = $theta2")
        println("  θ₃(0|i) = $theta3") 
        println("  θ₄(0|i) = $theta4")
    }
    
    @Test
    fun testEInvariantsComputation() {
        val p = 2.0
        val q = 3.0
        
        val invariants = Weierstrass.computeInvariants(p, q)
        
        // Check that e₁ + e₂ + e₃ = 0 (fundamental relation)
        val sum = invariants.e1 + invariants.e2 + invariants.e3
        assertTrue(abs(sum) < TOLERANCE, "e₁ + e₂ + e₃ should equal 0, got $sum")
        
        // Check that m = (e₂ - e₃)/(e₁ - e₃) is in valid range for Jacobi functions
        assertTrue(invariants.m > 0, "Jacobi parameter m should be positive")
        assertTrue(invariants.m < 1, "Jacobi parameter m should be less than 1")
        
        println("Lattice invariants for p=$p, q=$q:")
        println("  e₁ = ${invariants.e1}")
        println("  e₂ = ${invariants.e2}")
        println("  e₃ = ${invariants.e3}")
        println("  m = ${invariants.m}")
        println("  g₂ = ${invariants.g2}")
        println("  g₃ = ${invariants.g3}")
    }
    
    @Test
    fun testJacobiIdentities() {
        val u = HipparchusComplex(0.5, 0.3)
        val m = 0.7
        
        val (sn, cn, dn) = Jacobi.jacobiHipparchusComplex(u, m)
        
        // Test fundamental Jacobi identity: sn² + cn² = 1
        val identity1 = sn.multiply(sn).add(cn.multiply(cn))
        val error1 = identity1.subtract(HipparchusComplex.ONE).abs()
        assertTrue(error1 < TOLERANCE, "sn² + cn² = 1 failed, error = $error1")
        
        // Test second identity: dn² + m·sn² = 1
        val identity2 = dn.multiply(dn).add(sn.multiply(sn).multiply(m))
        val error2 = identity2.subtract(HipparchusComplex.ONE).abs()
        assertTrue(error2 < TOLERANCE, "dn² + m·sn² = 1 failed, error = $error2")
        
        println("Jacobi function values at u=$u, m=$m:")
        println("  sn = $sn")
        println("  cn = $cn")
        println("  dn = $dn")
        println("  sn² + cn² - 1 = ${identity1.subtract(HipparchusComplex.ONE)}")
        println("  dn² + m·sn² - 1 = ${identity2.subtract(HipparchusComplex.ONE)}")
    }
    
    @Test
    fun testWeierstrassDifferentialEquation() {
        val p = 2.0
        val q = 3.0
        
        // Test at several points
        val testPoints = listOf(
            HipparchusComplex(p/4.0, q/4.0),
            HipparchusComplex(p/3.0, q/5.0),
            HipparchusComplex(p/6.0, q/2.0)
        )
        
        for (z in testPoints) {
            val error = Weierstrass.verifyDifferentialEquation(z, p, q)
            val errorMagnitude = error.abs()
            
            assertTrue(
                errorMagnitude < 1e-8, 
                "Differential equation (℘')² = 4℘³ - g₂℘ - g₃ failed at z=$z, error=$errorMagnitude"
            )
            
            println("Differential equation verification at z=$z: error = $errorMagnitude")
        }
    }
    
    @Test
    fun testSquareLatticeSpecialCase() {
        // For square lattice (p = q), g₃ should be zero
        val p = 2.0
        val q = 2.0  // Square lattice
        
        val g3 = Weierstrass.g3(p, q)
        assertTrue(abs(g3) < 1e-6, "For square lattice, g₃ should be ≈ 0, got $g3")
        
        println("Square lattice g₃ = $g3 (should be ≈ 0)")
    }
    
    @Test
    fun testWeierstrassFunctionSymmetries() {
        val p = 2.0
        val q = 3.0
        val z = HipparchusComplex(0.5, 0.7)
        
        // Test ℘ function is even: ℘(-z) = ℘(z)
        val wpZ = Weierstrass.wp(z, p, q)
        val wpMinusZ = Weierstrass.wp(z.negate(), p, q)
        val evenError = wpZ.subtract(wpMinusZ).abs()
        assertTrue(evenError < TOLERANCE, "℘ should be even: ℘(-z) = ℘(z), error = $evenError")
        
        // Test ℘' function is odd: ℘'(-z) = -℘'(z)
        val wpPrimeZ = Weierstrass.wpPrime(z, p, q)
        val wpPrimeMinusZ = Weierstrass.wpPrime(z.negate(), p, q)
        val oddError = wpPrimeZ.add(wpPrimeMinusZ).abs()
        assertTrue(oddError < TOLERANCE, "℘' should be odd: ℘'(-z) = -℘'(z), error = $oddError")
        
        println("Symmetry tests:")
        println("  ℘ even symmetry error: $evenError")
        println("  ℘' odd symmetry error: $oddError")
    }
    
    @Test  
    fun testThetaSeriesConvergence() {
        // Test that theta series converge properly for typical lattice
        val p = 1.0
        val q = 2.0
        
        val (theta2, theta3, theta4) = Theta.thetaConstants(p, q)
        
        // All theta constants should be finite and non-zero
        assertTrue(theta2.isFinite(), "θ₂ should be finite")
        assertTrue(theta3.isFinite(), "θ₃ should be finite") 
        assertTrue(theta4.isFinite(), "θ₄ should be finite")
        
        assertTrue(theta2.abs() > 0, "θ₂ should be non-zero")
        assertTrue(theta3.abs() > 0, "θ₃ should be non-zero")
        assertTrue(theta4.abs() > 0, "θ₄ should be non-zero")
        
        println("Theta constants convergence test:")
        println("  θ₂ = $theta2 (|θ₂| = ${theta2.abs()})")
        println("  θ₃ = $theta3 (|θ₃| = ${theta3.abs()})")
        println("  θ₄ = $theta4 (|θ₄| = ${theta4.abs()})")
    }
}