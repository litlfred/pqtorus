import { Complex } from './ellipticMath'

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
 * Project complex lattice points to 3D torus surface
 */
function projectToTorus(
  latticePoints: Complex[], 
  period1: Complex, 
  period2: Complex,
  meshDensity: number
): Vertex3D[] {
  const vertices: Vertex3D[] = []
  
  // Create a regular torus parametrization
  const majorRadius = 2.0
  const minorRadius = 0.5
  
  for (let i = 0; i < meshDensity; i++) {
    for (let j = 0; j < meshDensity; j++) {
      const u = 2 * Math.PI * i / meshDensity
      const v = 2 * Math.PI * j / meshDensity
      
      const x = (majorRadius + minorRadius * Math.cos(v)) * Math.cos(u)
      const y = (majorRadius + minorRadius * Math.cos(v)) * Math.sin(u)
      const z = minorRadius * Math.sin(v)
      
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
 * Main function to generate torus geometry
 */
export function generateTorusGeometry(
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
  
  // Project to torus surface and create 3D vertices
  const vertices = projectToTorus(latticePoints, period1, period2, meshDensity)
  
  // Generate facets (quadrilaterals)
  const facets = generateFacets(meshDensity)
  
  // Calculate elliptic invariants (simplified)
  const jInvariant = new Complex(1728, 0) // Placeholder
  const discriminant = period1.multiply(period2)
  
  return {
    vertices,
    facets,
    jInvariant,
    discriminant,
    tau
  }
}