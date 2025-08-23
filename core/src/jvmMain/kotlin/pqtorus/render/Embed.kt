package pqtorus.render

import org.hipparchus.complex.Complex as HipparchusComplex
import pqtorus.math.Weierstrass

/**
 * Main embedding functionality for the Hipparchus-based Weierstrass elliptic functions.
 * Provides 3D embedding: (X,Y,Z) = A · (Re ℘, Im ℘, Re ℘′, Im ℘′)
 * 
 * This is the main API for the JVM implementation using Hipparchus for numerical computations.
 */

/**
 * Core embedding function: map complex point z to 3D coordinates.
 * 
 * @param z Complex point to embed (often z = u·p + v·q·i for (u,v) ∈ [0,1)²)
 * @param p First lattice period (real)
 * @param q Second lattice period (real, forms q·i imaginary period)
 * @param A Projection matrix (3x4) for embedding
 * @return 3D point (X, Y, Z)
 */
fun embed(z: HipparchusComplex, p: Double, q: Double, A: Matrix3x4): Vec3 {
    return Projection.embed(z, p, q, A)
}

/**
 * Convenience function for embedding with default projection matrix.
 * Uses basepoint z0 = p/3 + (q·i)/3 for matrix construction.
 */
fun embedWithDefaultProjection(z: HipparchusComplex, p: Double, q: Double): Vec3 {
    val A = Projection.buildDefaultProjectionMatrix(p, q)
    return embed(z, p, q, A)
}

/**
 * Generate a grid of embedded points for visualization.
 * Samples (u,v) grid over [0,1)² and maps to lattice points z = u·p + v·q·i.
 * 
 * @param p First lattice period
 * @param q Second lattice period  
 * @param gridSize Number of samples per dimension (gridSize × gridSize total points)
 * @param A Optional projection matrix (uses default if null)
 * @return List of 3D points representing the embedded torus surface
 */
fun generateEmbeddedGrid(
    p: Double, 
    q: Double, 
    gridSize: Int = 20,
    A: Matrix3x4? = null
): List<Vec3> {
    val projectionMatrix = A ?: Projection.buildDefaultProjectionMatrix(p, q)
    val points = mutableListOf<Vec3>()
    
    for (i in 0 until gridSize) {
        for (j in 0 until gridSize) {
            val u = i.toDouble() / gridSize
            val v = j.toDouble() / gridSize
            
            // Map (u,v) to lattice point z = u·p + v·q·i
            val z = HipparchusComplex(u * p, v * q)
            
            val point3D = embed(z, p, q, projectionMatrix)
            points.add(point3D)
        }
    }
    
    return points
}

/**
 * Generate mesh faces for a grid of points.
 * Creates quadrilateral faces connecting adjacent grid points.
 * 
 * @param gridSize Size of the grid (gridSize × gridSize points)
 * @return List of quadrilateral faces, each represented as 4 vertex indices
 */
fun generateGridFaces(gridSize: Int): List<IntArray> {
    val faces = mutableListOf<IntArray>()
    
    for (i in 0 until gridSize - 1) {
        for (j in 0 until gridSize - 1) {
            // Create quadrilateral face with vertices in counter-clockwise order
            val v0 = i * gridSize + j
            val v1 = i * gridSize + (j + 1)
            val v2 = (i + 1) * gridSize + (j + 1)
            val v3 = (i + 1) * gridSize + j
            
            faces.add(intArrayOf(v0, v1, v2, v3))
        }
    }
    
    return faces
}

/**
 * Data class representing a complete embedded torus mesh.
 */
data class EmbeddedTorus(
    val vertices: List<Vec3>,
    val faces: List<IntArray>,
    val latticeParams: LatticeParams,
    val projectionMatrix: Matrix3x4
) {
    /**
     * Export vertices to OBJ format string.
     */
    fun toOBJ(): String {
        val sb = StringBuilder()
        sb.appendLine("# Embedded torus with lattice periods p=${latticeParams.p}, q=${latticeParams.q}")
        sb.appendLine()
        
        // Write vertices
        for (vertex in vertices) {
            sb.appendLine("v ${vertex.x} ${vertex.y} ${vertex.z}")
        }
        sb.appendLine()
        
        // Write faces (OBJ uses 1-based indexing)
        for (face in faces) {
            sb.append("f")
            for (vertexIndex in face) {
                sb.append(" ${vertexIndex + 1}")
            }
            sb.appendLine()
        }
        
        return sb.toString()
    }
    
    /**
     * Export vertices to PLY format string.
     */
    fun toPLY(): String {
        val sb = StringBuilder()
        sb.appendLine("ply")
        sb.appendLine("format ascii 1.0")
        sb.appendLine("comment Embedded torus with lattice periods p=${latticeParams.p}, q=${latticeParams.q}")
        sb.appendLine("element vertex ${vertices.size}")
        sb.appendLine("property float x")
        sb.appendLine("property float y")
        sb.appendLine("property float z")
        sb.appendLine("element face ${faces.size}")
        sb.appendLine("property list uchar int vertex_index")
        sb.appendLine("end_header")
        
        // Write vertices
        for (vertex in vertices) {
            sb.appendLine("${vertex.x} ${vertex.y} ${vertex.z}")
        }
        
        // Write faces
        for (face in faces) {
            sb.append("${face.size}")
            for (vertexIndex in face) {
                sb.append(" $vertexIndex")
            }
            sb.appendLine()
        }
        
        return sb.toString()
    }
    
    /**
     * Export vertices to CSV format string.
     */
    fun toCSV(): String {
        val sb = StringBuilder()
        sb.appendLine("x,y,z")
        for (vertex in vertices) {
            sb.appendLine("${vertex.x},${vertex.y},${vertex.z}")
        }
        return sb.toString()
    }
}

/**
 * Data class for lattice parameters.
 */
data class LatticeParams(val p: Double, val q: Double)

/**
 * Generate a complete embedded torus mesh.
 * 
 * @param p First lattice period
 * @param q Second lattice period
 * @param gridSize Number of samples per dimension
 * @param z0 Optional basepoint for projection (uses default if null)
 * @return Complete embedded torus mesh ready for export or rendering
 */
fun generateEmbeddedTorus(
    p: Double,
    q: Double, 
    gridSize: Int = 20,
    z0: HipparchusComplex? = null
): EmbeddedTorus {
    val projectionMatrix = if (z0 != null) {
        Projection.buildProjectionMatrix(p, q, z0)
    } else {
        Projection.buildDefaultProjectionMatrix(p, q)
    }
    
    val vertices = generateEmbeddedGrid(p, q, gridSize, projectionMatrix)
    val faces = generateGridFaces(gridSize)
    
    return EmbeddedTorus(
        vertices = vertices,
        faces = faces,
        latticeParams = LatticeParams(p, q),
        projectionMatrix = projectionMatrix
    )
}