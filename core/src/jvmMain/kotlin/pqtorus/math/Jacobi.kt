package pqtorus.math

import org.hipparchus.complex.Complex
import org.hipparchus.special.elliptic.jacobi.JacobiElliptic
import org.hipparchus.special.elliptic.jacobi.JacobiEllipticBuilder
import kotlin.math.*

/**
 * Jacobi elliptic function wrappers using Hipparchus for both real and complex cases.
 * Provides sn(u|m), cn(u|m), dn(u|m) where m is the Jacobi parameter (aka k²).
 */
object Jacobi {
    
    /**
     * Compute Jacobi elliptic functions sn, cn, dn for real arguments.
     * @param u Real argument
     * @param m Jacobi parameter (k²)
     * @return Triple of (sn, cn, dn) values
     */
    fun jacobiReal(u: Double, m: Double): Triple<Double, Double, Double> {
        val jacobi = JacobiEllipticBuilder.build(m)
        val sn = jacobi.valuesN(u)
        return Triple(sn.sn(), sn.cn(), sn.dn())
    }
    
    /**
     * Compute Jacobi sn function for complex arguments using addition formulas.
     * For complex u = u₁ + i·u₂, we use the addition formula:
     * sn(u₁ + i·u₂|m) = (sn(u₁)·dn(u₂') + i·cn(u₁)·dn(u₁)·sn(u₂')·cn(u₂')) / (cn²(u₂') + m·sn²(u₁)·sn²(u₂'))
     * where m' = 1-m and u₂' corresponds to transformed argument.
     */
    fun snComplex(u: Complex, m: Double): Complex {
        val u1 = u.real
        val u2 = u.imaginary
        
        // Handle real case
        if (abs(u2) < 1e-15) {
            val (sn, _, _) = jacobiReal(u1, m)
            return Complex(sn, 0.0)
        }
        
        // For complex case, use transformation to complementary parameter
        val mPrime = 1.0 - m
        val k = sqrt(m)
        val kPrime = sqrt(mPrime)
        
        // Transform u₂ argument
        val u2Transformed = u2 * kPrime
        
        val (sn1, cn1, dn1) = jacobiReal(u1, m)
        val (sn2, cn2, dn2) = jacobiReal(u2Transformed, mPrime)
        
        // Apply addition formula for complex argument
        val numeratorReal = sn1 * dn2
        val numeratorImag = cn1 * dn1 * sn2 * cn2
        val denominator = cn2 * cn2 + m * sn1 * sn1 * sn2 * sn2
        
        return Complex(numeratorReal / denominator, numeratorImag / denominator)
    }
    
    /**
     * Compute Jacobi cn function for complex arguments.
     */
    fun cnComplex(u: Complex, m: Double): Complex {
        val u1 = u.real
        val u2 = u.imaginary
        
        // Handle real case
        if (abs(u2) < 1e-15) {
            val (_, cn, _) = jacobiReal(u1, m)
            return Complex(cn, 0.0)
        }
        
        val mPrime = 1.0 - m
        val kPrime = sqrt(mPrime)
        val u2Transformed = u2 * kPrime
        
        val (sn1, cn1, dn1) = jacobiReal(u1, m)
        val (sn2, cn2, dn2) = jacobiReal(u2Transformed, mPrime)
        
        // Addition formula for cn
        val numeratorReal = cn1 * cn2
        val numeratorImag = -sn1 * dn1 * sn2 * dn2
        val denominator = cn2 * cn2 + m * sn1 * sn1 * sn2 * sn2
        
        return Complex(numeratorReal / denominator, numeratorImag / denominator)
    }
    
    /**
     * Compute Jacobi dn function for complex arguments.
     */
    fun dnComplex(u: Complex, m: Double): Complex {
        val u1 = u.real
        val u2 = u.imaginary
        
        // Handle real case
        if (abs(u2) < 1e-15) {
            val (_, _, dn) = jacobiReal(u1, m)
            return Complex(dn, 0.0)
        }
        
        val mPrime = 1.0 - m
        val kPrime = sqrt(mPrime)
        val u2Transformed = u2 * kPrime
        
        val (sn1, cn1, dn1) = jacobiReal(u1, m)
        val (sn2, cn2, dn2) = jacobiReal(u2Transformed, mPrime)
        
        // Addition formula for dn
        val numeratorReal = dn1 * cn2 * dn2
        val numeratorImag = -m * sn1 * cn1 * sn2
        val denominator = cn2 * cn2 + m * sn1 * sn1 * sn2 * sn2
        
        return Complex(numeratorReal / denominator, numeratorImag / denominator)
    }
    
    /**
     * Convenience function to compute all three Jacobi functions at once for complex arguments.
     * @param u Complex argument
     * @param m Jacobi parameter (k²)
     * @return Triple of (sn, cn, dn) as Complex values
     */
    fun jacobiComplex(u: Complex, m: Double): Triple<Complex, Complex, Complex> {
        return Triple(
            snComplex(u, m),
            cnComplex(u, m),
            dnComplex(u, m)
        )
    }
    
    /**
     * Handle pole cases where sn(u|m) = 0 by applying small perturbation.
     * This prevents division by zero in Weierstrass function calculation.
     */
    fun snSafe(u: Complex, m: Double, epsilon: Double = 1e-12): Complex {
        val sn = snComplex(u, m)
        return if (sn.abs() < epsilon) {
            // Apply tiny perturbation to avoid pole
            val perturbedU = u.add(Complex(epsilon, epsilon))
            snComplex(perturbedU, m)
        } else {
            sn
        }
    }
}