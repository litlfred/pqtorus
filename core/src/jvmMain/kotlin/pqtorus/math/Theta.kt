package pqtorus.math

import org.hipparchus.complex.Complex
import kotlin.math.*

/**
 * Theta function constants and wrapper implementations using Hipparchus.
 * Implements θ₂(0|τ), θ₃(0|τ), θ₄(0|τ) at zero and θ₁(u|τ) for general u.
 */
object Theta {
    
    /**
     * Compute theta constant θ₂(0|τ) using series expansion.
     * θ₂(0|τ) = 2 * q^(1/4) * ∑_{n=0}^∞ q^(n(n+1)) where q = exp(iπτ)
     */
    fun theta2_0(tau: Complex): Complex {
        val q = (Complex.I.multiply(PI).multiply(tau)).exp()
        val qQuarter = q.pow(0.25)
        
        var sum = Complex.ZERO
        var term = Complex.ONE
        var n = 0
        
        // Series convergence: continue until term is negligible
        while (n < 100 && term.abs() > 1e-15) {
            val exponent = n * (n + 1)
            term = q.pow(exponent.toDouble())
            sum = sum.add(term)
            n++
        }
        
        return qQuarter.multiply(2.0).multiply(sum)
    }
    
    /**
     * Compute theta constant θ₃(0|τ) using series expansion.
     * θ₃(0|τ) = 1 + 2 * ∑_{n=1}^∞ q^(n²) where q = exp(iπτ)
     */
    fun theta3_0(tau: Complex): Complex {
        val q = (Complex.I.multiply(PI).multiply(tau)).exp()
        
        var sum = Complex.ONE
        var n = 1
        
        // Series convergence
        while (n < 100) {
            val exponent = n * n
            val term = q.pow(exponent.toDouble())
            if (term.abs() < 1e-15) break
            sum = sum.add(term.multiply(2.0))
            n++
        }
        
        return sum
    }
    
    /**
     * Compute theta constant θ₄(0|τ) using series expansion.
     * θ₄(0|τ) = 1 + 2 * ∑_{n=1}^∞ (-1)^n * q^(n²) where q = exp(iπτ)
     */
    fun theta4_0(tau: Complex): Complex {
        val q = (Complex.I.multiply(PI).multiply(tau)).exp()
        
        var sum = Complex.ONE
        var n = 1
        
        // Series convergence
        while (n < 100) {
            val exponent = n * n
            val term = q.pow(exponent.toDouble())
            if (term.abs() < 1e-15) break
            
            val sign = if (n % 2 == 0) 1.0 else -1.0
            sum = sum.add(term.multiply(sign * 2.0))
            n++
        }
        
        return sum
    }
    
    /**
     * Compute θ₁(u|τ) using series expansion.
     * θ₁(u|τ) = 2 * q^(1/4) * ∑_{n=0}^∞ (-1)^n * q^(n(n+1)) * sin((2n+1)πu)
     * where q = exp(iπτ)
     */
    fun theta1(u: Complex, tau: Complex): Complex {
        val q = (Complex.I.multiply(PI).multiply(tau)).exp()
        val qQuarter = q.pow(0.25)
        val piU = Complex(PI, 0.0).multiply(u)
        
        var sum = Complex.ZERO
        var n = 0
        
        // Series convergence
        while (n < 100) {
            val exponent = n * (n + 1)
            val qTerm = q.pow(exponent.toDouble())
            if (qTerm.abs() < 1e-15) break
            
            val angle = piU.multiply(Complex(2.0 * n + 1, 0.0))
            val sinTerm = angle.multiply(Complex.I).exp().subtract(
                angle.multiply(Complex.I).negate().exp()
            ).divide(Complex(0.0, 2.0))
            
            val sign = if (n % 2 == 0) 1.0 else -1.0
            val term = qTerm.multiply(sinTerm).multiply(sign)
            sum = sum.add(term)
            n++
        }
        
        return qQuarter.multiply(2.0).multiply(sum)
    }
    
    /**
     * Calculate all theta constants for τ = i·(q/p) for the rectangular lattice.
     * Returns (θ₂(0), θ₃(0), θ₄(0)) for the given lattice parameters.
     */
    fun thetaConstants(p: Double, q: Double): Triple<Complex, Complex, Complex> {
        val tau = Complex(0.0, q / p)
        return Triple(
            theta2_0(tau),
            theta3_0(tau),
            theta4_0(tau)
        )
    }
}