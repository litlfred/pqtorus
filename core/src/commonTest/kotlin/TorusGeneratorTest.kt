package com.pqtorus.core

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class TorusGeneratorTest {
    
    @Test
    fun testComplexArithmetic() {
        val a = Complex(1.0, 2.0)
        val b = Complex(3.0, 4.0)
        
        val sum = a + b
        assertEquals(4.0, sum.real)
        assertEquals(6.0, sum.imag)
        
        val product = a * b
        assertEquals(-5.0, product.real) // (1*3 - 2*4)
        assertEquals(10.0, product.imag) // (1*4 + 2*3)
    }
    
    @Test
    fun testPrimeChecking() {
        assertTrue(isPrime(2))
        assertTrue(isPrime(3))
        assertTrue(isPrime(5))
        assertTrue(isPrime(7))
        assertTrue(!isPrime(4))
        assertTrue(!isPrime(6))
        assertTrue(!isPrime(8))
    }
    
    @Test
    fun testNextPrime() {
        assertEquals(2, nextPrime(1))
        assertEquals(3, nextPrime(3))
        assertEquals(5, nextPrime(4))
        assertEquals(7, nextPrime(6))
    }
    
    @Test
    fun testTorusGeneration() {
        val generator = TorusGenerator()
        val geometry = generator.generateTorus(2.0, 3.0, 1, 10)
        
        // Basic sanity checks
        assertTrue(geometry.vertices.isNotEmpty())
        assertTrue(geometry.facets.isNotEmpty())
        assertEquals(100, geometry.vertices.size) // 10x10 mesh
        assertEquals(100, geometry.facets.size)   // 10x10 facets
    }
}