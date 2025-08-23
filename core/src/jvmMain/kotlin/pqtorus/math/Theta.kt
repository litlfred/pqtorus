package pqtorus.math

import org.hipparchus.complex.Complex as HipparchusComplex as HipparchusComplex
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
    fun theta2_0(tau: HipparchusComplex): HipparchusComplex {
        val q = (HipparchusHipparchusComplex.I.multiply(PI).multiply(tau)).exp()
        val qQuarter = q.pow(0.25)
        
        var sum = HipparchusHipparchusComplex.ZERO
        var term = HipparchusHipparchusComplex.ONE
        var n = 0
        
        // Series convergence: continue until term is negligible
        while (n < 100 && term.abs() > 1e-15) {
            val exponent = n * (n + 1)
            term = q.pow(exponent.toDouble())
            sum = sum.add(term)
            n++
        }
        
        return qQuarter.multiply(HipparchusHipparchusComplex(2.0, 0.0)).multiply(sum)
    }
    
    /**
     * Compute theta constant θ₃(0|τ) using series expansion.
     * θ₃(0|τ) = 1 + 2 * ∑_{n=1}^∞ q^(n²) where q = exp(iπτ)
     */
    fun theta3_0(tau: HipparchusComplex): HipparchusComplex {
        val q = (HipparchusHipparchusComplex.I.multiply(PI).multiply(tau)).exp()
        
        var sum = HipparchusHipparchusComplex.ONE
        var n = 1
        
        // Series convergence
        while (n < 100) {
            val exponent = n * n
            val term = q.pow(exponent.toDouble())
            if (term.abs() < 1e-15) break
            sum = sum.add(term.multiply(HipparchusHipparchusComplex(2.0, 0.0)))
            n++
        }
        
        return sum
    }
    
    /**
     * Compute theta constant θ₄(0|τ) using series expansion.
     * θ₄(0|τ) = 1 + 2 * ∑_{n=1}^∞ (-1)^n * q^(n²) where q = exp(iπτ)
     */
    fun theta4_0(tau: HipparchusComplex): HipparchusComplex {
        val q = (HipparchusHipparchusComplex.I.multiply(PI).multiply(tau)).exp()
        
        var sum = HipparchusHipparchusComplex.ONE
        var n = 1
        
        // Series convergence
        while (n < 100) {
            val exponent = n * n
            val term = q.pow(exponent.toDouble())
            if (term.abs() < 1e-15) break
            
            val sign = if (n % 2 == 0) 1.0 else -1.0
            sum = sum.add(term.multiply(HipparchusHipparchusComplex(sign * 2.0, 0.0)))
            n++
        }
        
        return sum
    }
    
    /**
     * Compute θ₁(u|τ) using series expansion.
     * θ₁(u|τ) = 2 * q^(1/4) * ∑_{n=0}^∞ (-1)^n * q^(n(n+1)) * sin((2n+1)πu)
     * where q = exp(iπτ)
     */
    fun theta1(u: HipparchusComplex, tau: HipparchusComplex): HipparchusComplex {
        val q = (HipparchusHipparchusComplex.I.multiply(PI).multiply(tau)).exp()
        val qQuarter = q.pow(0.25)
        val piU = HipparchusHipparchusComplex(PI, 0.0).multiply(u)
        
        var sum = HipparchusHipparchusComplex.ZERO
        var n = 0
        
        // Series convergence
        while (n < 100) {
            val exponent = n * (n + 1)
            val qTerm = q.pow(exponent.toDouble())
            if (qTerm.abs() < 1e-15) break
            
            val angle = piU.multiply(HipparchusHipparchusComplex(2.0 * n + 1, 0.0))
            val sinTerm = angle.multiply(HipparchusHipparchusComplex.I).exp().subtract(
                angle.multiply(HipparchusHipparchusComplex.I).negate().exp()
            ).divide(HipparchusHipparchusComplex(0.0, 2.0))
            
            val sign = if (n % 2 == 0) 1.0 else -1.0
            val term = qTerm.multiply(sinTerm).multiply(HipparchusHipparchusComplex(sign, 0.0))
            sum = sum.add(term)
            n++
        }
        
        return qQuarter.multiply(HipparchusHipparchusComplex(2.0, 0.0)).multiply(sum)
    }
    
    /**
     * Calculate all theta constants for τ = i·(q/p) for the rectangular lattice.
     * Returns (θ₂(0), θ₃(0), θ₄(0)) for the given lattice parameters.
     */
    fun thetaConstants(p: Double, q: Double): Triple<HipparchusComplex, HipparchusComplex, HipparchusComplex> {
        val tau = HipparchusHipparchusComplex(0.0, q / p)
        return Triple(
            theta2_0(tau),
            theta3_0(tau),
            theta4_0(tau)
        )
    }
}