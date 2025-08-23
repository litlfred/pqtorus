package pqtorus.render

import org.hipparchus.complex.Complex as HipparchusComplex
import pqtorus.math.Weierstrass
import kotlin.math.*

/**
 * 3D projection matrix and vector classes for embedding the complex torus.
 */
data class Vec3(val x: Double, val y: Double, val z: Double) {
    operator fun plus(other: Vec3) = Vec3(x + other.x, y + other.y, z + other.z)
    operator fun minus(other: Vec3) = Vec3(x - other.x, y - other.y, z - other.z)
    operator fun times(scalar: Double) = Vec3(x * scalar, y * scalar, z * scalar)
    
    fun magnitude() = sqrt(x * x + y * y + z * z)
    fun normalize() = this * (1.0 / magnitude())
}

/**
 * 3x4 matrix for projecting 4D Weierstrass coordinates to 3D space.
 * Stores three row vectors, each of length 4.
 */
data class Matrix3x4(val r1: DoubleArray, val r2: DoubleArray, val r3: DoubleArray) {
    init {
        require(r1.size == 4 && r2.size == 4 && r3.size == 4) { "Each row must have length 4" }
    }
    
    /**
     * Multiply matrix by 4D vector phi = (Re ℘, Im ℘, Re ℘′, Im ℘′).
     * Returns 3D vector (X, Y, Z).
     */
    fun multiply(phi: DoubleArray): Vec3 {
        require(phi.size == 4) { "phi must have length 4" }
        val x = r1[0]*phi[0] + r1[1]*phi[1] + r1[2]*phi[2] + r1[3]*phi[3]
        val y = r2[0]*phi[0] + r2[1]*phi[1] + r2[2]*phi[2] + r2[3]*phi[3]
        val z = r3[0]*phi[0] + r3[1]*phi[1] + r3[2]*phi[2] + r3[3]*phi[3]
        return Vec3(x, y, z)
    }
    
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false
        other as Matrix3x4
        return r1.contentEquals(other.r1) && r2.contentEquals(other.r2) && r3.contentEquals(other.r3)
    }
    
    override fun hashCode(): Int {
        var result = r1.contentHashCode()
        result = 31 * result + r2.contentHashCode()
        result = 31 * result + r3.contentHashCode()
        return result
    }
}

/**
 * Projection utilities for building lattice-aligned projection matrices.
 */
object Projection {
    
    /**
     * Build lattice-aligned projection matrix A from basepoint z0.
     * Uses the algorithm described in the specification:
     * 
     * Let y0 = ℘′(z0) and y0″ = 6·℘(z0)² - g2/2
     * Write y0 = y1 + i·y2, y0″ = y1′ + i·y2′
     * 
     * Define rows:
     * a1 = ( p·y1,  p·y2,  p·y1′,  p·y2′)
     * a2 = (-q·y2,  q·y1, -q·y2′,  q·y1′)
     * a3 = (    0,     0,      0,      1)
     * 
     * @param p First lattice period (real)
     * @param q Second lattice period (real, imaginary part)
     * @param z0 Basepoint for projection alignment
     * @return 3x4 projection matrix A
     */
    fun buildProjectionMatrix(p: Double, q: Double, z0: HipparchusComplex): Matrix3x4 {
        // Compute Weierstrass functions at basepoint
        val wp0 = Weierstrass.wp(z0, p, q)
        val wpPrime0 = Weierstrass.wpPrime(z0, p, q)
        
        // Compute second derivative: y0″ = 6·℘(z0)² - g2/2
        val g2 = Weierstrass.g2(p, q)
        val wpPrimePrime0 = wp0.multiply(wp0).multiply(6.0).subtract(HipparchusComplex(g2 / 2.0, 0.0))
        
        // Extract real and imaginary parts
        val y1 = wpPrime0.real        // Re ℘′(z0)
        val y2 = wpPrime0.imaginary   // Im ℘′(z0)
        val y1Prime = wpPrimePrime0.real      // Re ℘″(z0)
        val y2Prime = wpPrimePrime0.imaginary // Im ℘″(z0)
        
        // Build projection matrix rows
        val a1 = doubleArrayOf(p * y1, p * y2, p * y1Prime, p * y2Prime)
        val a2 = doubleArrayOf(-q * y2, q * y1, -q * y2Prime, q * y1Prime)
        val a3 = doubleArrayOf(0.0, 0.0, 0.0, 1.0)
        
        return Matrix3x4(a1, a2, a3)
    }
    
    /**
     * Build default projection matrix using recommended basepoint z0 = p/3 + (q·i)/3.
     * This provides a good general-purpose projection for most lattices.
     */
    fun buildDefaultProjectionMatrix(p: Double, q: Double): Matrix3x4 {
        val z0 = HipparchusComplex(p / 3.0, q / 3.0)
        return buildProjectionMatrix(p, q, z0)
    }
    
    /**
     * Convert Weierstrass function values to 4D coordinate vector Φ(z).
     * Φ(z) = (Re ℘(z), Im ℘(z), Re ℘′(z), Im ℘′(z))
     */
    fun weierstrassTo4D(z: HipparchusComplex, p: Double, q: Double): DoubleArray {
        val wp = Weierstrass.wp(z, p, q)
        val wpPrime = Weierstrass.wpPrime(z, p, q)
        
        return doubleArrayOf(
            wp.real,
            wp.imaginary,
            wpPrime.real,
            wpPrime.imaginary
        )
    }
    
    /**
     * Apply projection matrix to embed a complex point z into 3D space.
     * Returns (X, Y, Z) = A · Φ(z) where Φ(z) is the 4D Weierstrass coordinate.
     */
    fun embed(z: HipparchusComplex, p: Double, q: Double, projectionMatrix: Matrix3x4): Vec3 {
        val phi = weierstrassTo4D(z, p, q)
        return projectionMatrix.multiply(phi)
    }
}