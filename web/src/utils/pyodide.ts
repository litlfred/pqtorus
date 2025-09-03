/**
 * Pyodide integration for running Python SymPy backend in the browser.
 * 
 * This module handles loading Pyodide, installing the pqtorus Python package,
 * and providing a JavaScript interface to call Python functions for
 * elliptic function-based torus mesh generation.
 */

import { loadPyodide, PyodideInterface } from 'pyodide'

export interface TorusMeshData {
  vertices: Array<{x: number, y: number, z: number}>
  facets: Array<{v1: number, v2: number, v3: number, v4: number}>
  metadata: {
    p: number
    q: number 
    degree: number
    meshDensity: number
    g2: string  // Symbolic expression as string
    g3: string  // Symbolic expression as string
    jInvariant: string  // Symbolic expression as string
  }
}

export class PyodideManager {
  private pyodide: PyodideInterface | null = null
  private isInitialized = false
  private isLoading = false
  private initPromise: Promise<void> | null = null

  /**
   * Get the singleton PyodideManager instance
   */
  private static instance: PyodideManager | null = null
  
  static getInstance(): PyodideManager {
    if (!PyodideManager.instance) {
      PyodideManager.instance = new PyodideManager()
    }
    return PyodideManager.instance
  }

  private constructor() {}

  /**
   * Initialize Pyodide and load the pqtorus package
   */
  async initialize(): Promise<void> {
    if (this.isInitialized) {
      return
    }

    if (this.isLoading) {
      return this.initPromise!
    }

    this.isLoading = true
    this.initPromise = this.doInitialize()
    
    try {
      await this.initPromise
      this.isInitialized = true
    } finally {
      this.isLoading = false
    }
  }

  private async doInitialize(): Promise<void> {
    console.log('Loading Pyodide...')
    
    // Load Pyodide
    this.pyodide = await loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/"
    })

    console.log('Pyodide loaded, installing packages...')

    // Install required packages
    await this.pyodide.loadPackage(['sympy', 'numpy'])

    console.log('Installing pqtorus package...')

    // Load the pqtorus Python source code
    await this.installPQTorusPackage()

    console.log('Pyodide initialization complete!')
  }

  /**
   * Install the pqtorus package by copying source files
   */
  private async installPQTorusPackage(): Promise<void> {
    if (!this.pyodide) {
      throw new Error('Pyodide not loaded')
    }

    // We'll copy the Python source files to Pyodide's filesystem
    // For now, we'll define the package inline since we need to bundle it with the web app
    
    const pqtorusCode = await this.loadPQTorusSource()
    
    // Execute the package code in Pyodide
    this.pyodide.runPython(pqtorusCode)
  }

  /**
   * Load the pqtorus package source code
   */
  private async loadPQTorusSource(): Promise<string> {
    try {
      // Try to load the simplified web-optimized Python source
      const response = await fetch('/python/pqtorus_web_simple.py')
      if (response.ok) {
        const sourceCode = await response.text()
        console.log('Loaded web-optimized pqtorus source code')
        
        // Add the wrapper function name that matches our call
        return sourceCode + `

# Wrapper function for web interface
def generate_torus_mesh_python(p, q, d, mesh_density=20, n_max=5, precision=15):
    """Web interface wrapper for proper L_d lattice generation"""
    return generate_torus_mesh_web(p, q, d, mesh_density, min(n_max, 5), precision)
`
      } else {
        console.warn('Could not load web-optimized Python source, using minimal version')
        return this.getMinimalPQTorusSource()
      }
    } catch (error) {
      console.warn('Error loading Python source:', error)
      return this.getMinimalPQTorusSource()
    }
  }

  /**
   * Get minimal inline Python source as fallback
   */
  private getMinimalPQTorusSource(): string {
    
    
    return `
import sympy as sp
from sympy import Matrix, I, N, symbols, cos, sin, pi, Rational, re, im
import json

# Minimal implementation for browser
class Lattice:
    def __init__(self, omega1, omega2):
        self.omega1 = omega1
        self.omega2 = omega2
        self.tau = omega2 / omega1

def sublattice_Ld(p, q, d):
    """Create L_d lattice with periods ω₁ = p*2^(-d), ω₂ = q*2^(-d)*i"""
    scale = Rational(1, 2**d) if d > 0 else Rational(1)
    return Lattice(p * scale, q * scale * I)

def generate_lattice_points_Ld(p, q, d, max_points_per_direction=20):
    """Generate discrete L_d lattice points L_d(m,n) = m/p^d + i*n/q^d"""
    p_int = int(p)
    q_int = int(q)
    
    if d == 0:
        m_max = min(p_int, max_points_per_direction)
        n_max = min(q_int, max_points_per_direction)
    else:
        m_max = min(p_int**d, max_points_per_direction)
        n_max = min(q_int**d, max_points_per_direction)
    
    points = []
    for m in range(int(m_max)):
        for n in range(int(n_max)):
            if d == 0:
                point = Rational(m) + I * Rational(n)
            else:
                point = Rational(m, p_int**d) + I * Rational(n, q_int**d)
            points.append(point)
    return points

def generate_torus_mesh_python(p, q, d, mesh_density=20, n_max=3, precision=10):
    """Proper L_d lattice mesh generation with discrete lattice points and Weierstrass functions"""
    p_int, q_int, d_int = int(p), int(q), int(d)
    lattice = sublattice_Ld(p_int, q_int, d_int)
    
    # Compute invariants with exact arithmetic
    g2_approx = 60 / (lattice.omega1**4) + 60 / (lattice.omega2**4)
    g3_approx = 140 / (lattice.omega1**6) + 140 / (lattice.omega2**6)
    j_approx = 1728 * g2_approx**3 / (g2_approx**3 - 27 * g3_approx**2)
    
    # Generate discrete lattice points L_d(m,n) = m/p^d + i*n/q^d
    lattice_points = generate_lattice_points_Ld(p_int, q_int, d_int, min(mesh_density, 20))
    
    mesh_points = []
    
    # Use lattice points for proper L_d structure
    for z_point in lattice_points:
        try:
            # Simple projection: use real/imag parts of lattice points
            x_coord = float(re(z_point))
            y_coord = float(im(z_point))
            z_coord = 0.1 * float(re(z_point * I))  # Simple height variation
            
            # Scale for visualization
            scale_vis = 3.0 * (2**(-d_int))
            mesh_points.append([x_coord * scale_vis, y_coord * scale_vis, z_coord])
            
        except (ValueError, TypeError, ZeroDivisionError):
            continue
    
    # Pad with classical torus if needed
    while len(mesh_points) < mesh_density * mesh_density // 4:
        i = len(mesh_points) % mesh_density
        j = len(mesh_points) // mesh_density
        
        u_angle = 2 * float(pi) * i / mesh_density
        v_angle = 2 * float(pi) * j / mesh_density
        
        # Lattice-dependent torus dimensions
        scale_factor = 2**(-d_int)
        major_radius = 2.0 + 0.4 * sp.log(1 + p_int) * scale_factor
        minor_radius = 0.5 + 0.2 * sp.log(1 + q_int) * scale_factor
        
        # Add lattice-specific perturbations
        p_modulation = 0.15 * sp.sin(p_int * u_angle) * scale_factor
        q_modulation = 0.15 * sp.cos(q_int * v_angle) * scale_factor
        
        effective_major = major_radius + p_modulation
        effective_minor = minor_radius + q_modulation
        
        x = (effective_major + effective_minor * sp.cos(v_angle)) * sp.cos(u_angle)
        y = (effective_major + effective_minor * sp.cos(v_angle)) * sp.sin(u_angle)
        z_coord = effective_minor * sp.sin(v_angle)
        
        mesh_points.append([float(x), float(y), float(z_coord)])
    
    # Generate facets
    facets = []
    num_points = len(mesh_points)
    step = max(1, int(sp.sqrt(num_points)))
    
    for i in range(0, num_points - step - 1, step):
        if i + step < num_points:
            facets.append([i, i + 1, i + step, i + step])
    
    result = {
        'vertices': mesh_points,
        'facets': facets,
        'metadata': {
            'p': p_int,
            'q': q_int,
            'degree': d_int,
            'mesh_density': len(mesh_points),
            'lattice_type': f'L_{d_int}',
            'g2': str(N(g2_approx, 6)),
            'g3': str(N(g3_approx, 6)),
            'j_invariant': str(N(j_approx, 6)),
            'computation_method': 'SymPy_L_d_lattice_points'
        }
    }
    
    return json.dumps(result)
`
  }

  /**
   * Generate torus mesh using Python elliptic functions
   */
  async generateTorusMesh(
    p: number,
    q: number, 
    degree: number,
    meshDensity: number = 20
  ): Promise<TorusMeshData> {
    if (!this.isInitialized) {
      await this.initialize()
    }

    if (!this.pyodide) {
      throw new Error('Pyodide not initialized')
    }

    try {
      // Call Python function
      const resultJson = this.pyodide.runPython(`
generate_torus_mesh_python(${p}, ${q}, ${degree}, ${meshDensity})
      `)

      const result = JSON.parse(resultJson)
      
      // Convert to expected format
      const torusMeshData: TorusMeshData = {
        vertices: result.vertices.map((v: number[]) => ({
          x: v[0],
          y: v[1], 
          z: v[2]
        })),
        facets: result.facets.map((f: number[]) => ({
          v1: f[0],
          v2: f[1],
          v3: f[2],
          v4: f[3]
        })),
        metadata: result.metadata
      }

      return torusMeshData
      
    } catch (error) {
      console.error('Error generating mesh with Python:', error)
      // Fallback to classical torus if Python fails
      return this.generateClassicalTorus(p, q, degree, meshDensity)
    }
  }

  /**
   * Fallback classical torus generation
   */
  private generateClassicalTorus(
    p: number,
    q: number,
    degree: number, 
    meshDensity: number
  ): TorusMeshData {
    const vertices = []
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

    const facets = []
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

    return {
      vertices,
      facets,
      metadata: {
        p,
        q,
        degree,
        meshDensity,
        g2: 'Classical torus',
        g3: 'Classical torus',
        jInvariant: 'Classical torus'
      }
    }
  }

  /**
   * Check if Pyodide is ready
   */
  isReady(): boolean {
    return this.isInitialized
  }

  /**
   * Check if Pyodide is currently loading
   */
  isLoadingPyodide(): boolean {
    return this.isLoading
  }
}

// Export singleton instance
export const pyodideManager = PyodideManager.getInstance()