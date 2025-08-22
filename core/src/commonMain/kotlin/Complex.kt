package com.pqtorus.core

/**
 * Represents a complex number with real and imaginary parts
 */
data class Complex(val real: Double, val imag: Double) {
    operator fun plus(other: Complex) = Complex(real + other.real, imag + other.imag)
    operator fun minus(other: Complex) = Complex(real - other.real, imag - other.imag)
    operator fun times(other: Complex) = Complex(
        real * other.real - imag * other.imag,
        real * other.imag + imag * other.real
    )
    operator fun times(scalar: Double) = Complex(real * scalar, imag * scalar)
    operator fun div(scalar: Double) = Complex(real / scalar, imag / scalar)
    operator fun div(other: Complex): Complex {
        val denominator = other.real * other.real + other.imag * other.imag
        return if (denominator != 0.0) {
            Complex(
                (real * other.real + imag * other.imag) / denominator,
                (imag * other.real - real * other.imag) / denominator
            )
        } else {
            Complex(0.0, 0.0) // Or throw an exception
        }
    }
    
    val magnitude: Double get() = kotlin.math.sqrt(real * real + imag * imag)
    val phase: Double get() = kotlin.math.atan2(imag, real)
    
    fun conjugate() = Complex(real, -imag)
    
    companion object {
        val ZERO = Complex(0.0, 0.0)
        val ONE = Complex(1.0, 0.0)
        val I = Complex(0.0, 1.0)
    }
}

/**
 * Represents a 3D vertex for rendering
 */
data class Vertex3D(val x: Double, val y: Double, val z: Double)

/**
 * Represents a quadrilateral facet with 4 vertices
 */
data class Facet(val v1: Int, val v2: Int, val v3: Int, val v4: Int)

/**
 * Geometry data for rendering the torus
 */
data class TorusGeometry(
    val vertices: List<Vertex3D>,
    val facets: List<Facet>,
    val jInvariant: Complex,
    val discriminant: Complex,
    val tau: Complex
)