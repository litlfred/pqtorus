package pqtorus.test

import org.hipparchus.complex.Complex as HipparchusComplex
import kotlin.math.PI

fun test() {
    val c = HipparchusComplex(1.0, 2.0)
    val d = c.multiply(2.0)    // Test if this works
    val e = c.multiply(HipparchusComplex(2.0, 0.0))  // Alternative
    
    val q = HipparchusComplex.I.multiply(PI)
    val abs = c.abs()
    val comparison = abs > 1e-15  // Test if this works
    
    println("Test successful")
}