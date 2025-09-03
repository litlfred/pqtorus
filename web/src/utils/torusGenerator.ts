import { Complex } from './ellipticMath'
import { pyodideManager, TorusMeshData } from './pyodide'

export interface Vertex3D {
  x: number
  y: number
  z: number
}

export interface Facet {
  v1: number
  v2: number
  v3: number
  v4: number
}

export interface TorusGeometry {
  vertices: Vertex3D[]
  facets: Facet[]
  jInvariant: Complex
  discriminant: Complex
  tau: Complex
  usePython?: boolean
  metadata?: {
    p: number
    q: number
    degree: number
    meshDensity: number
    g2: string
    g3: string
    jInvariant: string
  }
}

/**
 * Generate lattice points for degree d approximation
 */
function generateLatticePoints(period1: Complex, period2: Complex, degree: number): Complex[] {
  const points: Complex[] = []
  const scale = 1.0 / Math.pow(2, degree) // 2^(-degree)
  
  // Generate points in a reasonable range for visualization
  const range = 10
  for (let n1 = -range; n1 <= range; n1++) {
    for (let n2 = -range; n2 <= range; n2++) {
      const point = period1.scale(n1 * scale).add(period2.scale(n2 * scale))
      points.push(point)
    }
  }
  return points
}

/**
 * Project complex lattice points to 3D torus surface using lattice-dependent parameters
 */
function projectToTorus(
  latticePoints: Complex[], 
  period1: Complex, 
  period2: Complex,
  meshDensity: number,
  p: number,
  q: number,
  degree: number
): Vertex3D[] {
  const vertices: Vertex3D[] = []
  
  // Make torus parameters dependent on p, q, and degree
  // The lattice L_d = Z(p * 2^(-d)) + Z(q * 2^(-d) * i) should affect the torus shape
  const latticeScale = Math.pow(2, -degree)  // 2^(-d)
  const majorRadius = 2.0 + 0.5 * Math.log(p + 1) * latticeScale
  const minorRadius = 0.5 + 0.2 * Math.log(q + 1) * latticeScale
  
  // Add aspect ratio based on p/q ratio
  const aspectRatio = Math.min(p, q) / Math.max(p, q)
  const radiusModulation = 1.0 + 0.3 * (1 - aspectRatio)
  
  for (let i = 0; i < meshDensity; i++) {
    for (let j = 0; j < meshDensity; j++) {
      const u = 2 * Math.PI * i / meshDensity
      const v = 2 * Math.PI * j / meshDensity
      
      // Add lattice-inspired modulations
      const pModulation = 0.1 * Math.sin(p * u) * latticeScale
      const qModulation = 0.1 * Math.cos(q * v) * latticeScale
      const degreeModulation = 0.05 * Math.sin(degree * (u + v))
      
      const effectiveMajor = majorRadius * radiusModulation + pModulation
      const effectiveMinor = minorRadius + qModulation
      
      const x = (effectiveMajor + effectiveMinor * Math.cos(v)) * Math.cos(u)
      const y = (effectiveMajor + effectiveMinor * Math.cos(v)) * Math.sin(u)
      const z = effectiveMinor * Math.sin(v) + degreeModulation
      
      vertices.push({ x, y, z })
    }
  }
  
  return vertices
}

/**
 * Generate quadrilateral facets for the mesh
 */
function generateFacets(meshDensity: number): Facet[] {
  const facets: Facet[] = []
  
  for (let i = 0; i < meshDensity; i++) {
    for (let j = 0; j < meshDensity; j++) {
      const current = i * meshDensity + j
      const nextI = ((i + 1) % meshDensity) * meshDensity + j
      const nextJ = i * meshDensity + (j + 1) % meshDensity
      const nextBoth = ((i + 1) % meshDensity) * meshDensity + (j + 1) % meshDensity
      
      facets.push({
        v1: current,
        v2: nextI,
        v3: nextBoth,
        v4: nextJ
      })
    }
  }
  
  return facets
}

/**
 * Main function to generate torus geometry using Python elliptic functions
 */
export async function generateTorusGeometry(
  p: number,
  q: number,
  degree: number,
  meshDensity: number = 20,
  usePython: boolean = true
): Promise<TorusGeometry> {
  // Try Python implementation first if requested and available
  if (usePython && pyodideManager.isReady()) {
    try {
      const pythonResult = await pyodideManager.generateTorusMesh(p, q, degree, meshDensity)
      
      // Calculate tau for compatibility
      const period1 = new Complex(p, 0)
      const period2 = new Complex(0, q)
      const tau = period2.divide(period1)
      
      return {
        vertices: pythonResult.vertices,
        facets: pythonResult.facets,
        jInvariant: new Complex(parseFloat(pythonResult.metadata.jInvariant) || 1728, 0),
        discriminant: period1.multiply(period2),
        tau,
        usePython: true,
        metadata: pythonResult.metadata
      }
    } catch (error) {
      console.warn('Python mesh generation failed, falling back to classical:', error)
    }
  }

  // Fallback to classical torus generation
  return generateClassicalTorusGeometry(p, q, degree, meshDensity)
}

/**
 * Generate classical torus geometry (original implementation with lattice-dependent parameters)
 */
export function generateClassicalTorusGeometry(
  p: number,
  q: number,
  degree: number,
  meshDensity: number = 20
): TorusGeometry {
  // Create lattice periods
  const period1 = new Complex(p, 0)
  const period2 = new Complex(0, q)
  
  // Calculate tau = period2 / period1
  const tau = period2.divide(period1)
  
  // Generate lattice points for degree d approximation
  const latticePoints = generateLatticePoints(period1, period2, degree)
  
  // Project to torus surface with lattice-dependent parameters
  const vertices = projectToTorus(latticePoints, period1, period2, meshDensity, p, q, degree)
  
  // Generate facets (quadrilaterals)
  const facets = generateFacets(meshDensity)
  
  // Calculate elliptic invariants (approximated based on lattice)
  const latticeScale = Math.pow(2, -degree)
  const g2Approx = 60 * Math.pow(p * latticeScale, -4) + 60 * Math.pow(q * latticeScale, -4)
  const g3Approx = 140 * Math.pow(p * latticeScale, -6) + 140 * Math.pow(q * latticeScale, -6)
  const discriminant = Math.pow(g2Approx, 3) - 27 * Math.pow(g3Approx, 2)
  const jInvariant = discriminant !== 0 ? new Complex(1728 * Math.pow(g2Approx, 3) / discriminant, 0) : new Complex(1728, 0)
  
  return {
    vertices,
    facets,
    jInvariant,
    discriminant: period1.multiply(period2),
    tau,
    usePython: false,
    metadata: {
      p,
      q,
      degree,
      meshDensity,
      g2: g2Approx.toFixed(6),
      g3: g3Approx.toFixed(6), 
      jInvariant: jInvariant.real.toFixed(6)
    }
  }
}