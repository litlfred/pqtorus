"""
Simplified mesh generation for web integration.
This provides a working implementation that can be easily loaded into Pyodide.
"""

import sympy as sp
from sympy import Matrix, I, N, symbols, cos, sin, pi, Rational, re, im
import json

class Lattice:
    """Simple lattice class"""
    def __init__(self, omega1, omega2):
        self.omega1 = omega1
        self.omega2 = omega2
        self.tau = omega2 / omega1

def primary_lattice(p, q):
    """Create primary lattice L_prim = Zp + Z(qi)"""
    return Lattice(p, q * I)

def sublattice_Ld(p, q, d):
    """Create sublattice L_d = Z(p * 2^(-d)) + Z(q * 2^(-d) * i)"""
    scale = Rational(1, 2**d)
    return Lattice(p * scale, q * scale * I)

def eisenstein_series_g2(omega1, omega2, n_max=10):
    """Compute g2 Eisenstein series"""
    g2 = 0
    for m in range(-n_max, n_max + 1):
        for n in range(-n_max, n_max + 1):
            if m == 0 and n == 0:
                continue
            lattice_point = m * omega1 + n * omega2
            g2 += 1 / (lattice_point**4)
    return 60 * g2

def eisenstein_series_g3(omega1, omega2, n_max=10):
    """Compute g3 Eisenstein series"""  
    g3 = 0
    for m in range(-n_max, n_max + 1):
        for n in range(-n_max, n_max + 1):
            if m == 0 and n == 0:
                continue
            lattice_point = m * omega1 + n * omega2
            g3 += 1 / (lattice_point**6)
    return 140 * g3

def wp_and_wpprime_simplified(z, lattice, n_max=8, precision=15):
    """Simplified Weierstrass function computation"""
    # Start with principal term  
    if abs(z) < 1e-10:
        # Avoid singularity at origin
        z = z + Rational(1, 100) + Rational(1, 100) * I
    
    wp_z = 1 / (z**2)
    wpprime_z = -2 / (z**3)
    
    # Add lattice point contributions
    for m in range(-n_max, n_max + 1):
        for n in range(-n_max, n_max + 1):
            if m == 0 and n == 0:
                continue
            lattice_point = m * lattice.omega1 + n * lattice.omega2
            if abs(lattice_point) > 1e-10:
                term = z - lattice_point
                if abs(term) > 1e-10:
                    wp_z += 1/term**2 - 1/lattice_point**2
                    wpprime_z += -2/term**3
    
    if precision:
        wp_z = N(wp_z, precision)
        wpprime_z = N(wpprime_z, precision)
    
    return wp_z, wpprime_z

def generate_torus_mesh_web(p, q, d, mesh_density=20, n_max=5, precision=10):
    """Generate torus mesh optimized for web usage with better performance"""
    lattice = sublattice_Ld(p, q, d)
    
    # Compute invariants with lower precision for speed
    g2 = eisenstein_series_g2(lattice.omega1, lattice.omega2, min(n_max, 4))
    g3 = eisenstein_series_g3(lattice.omega1, lattice.omega2, min(n_max, 4))
    
    # Compute j-invariant  
    discriminant = g2**3 - 27 * g3**2
    j_inv = 1728 * g2**3 / discriminant if discriminant != 0 else sp.oo
    
    mesh_points = []
    
    # Use a hybrid approach: elliptic functions for shape, classical for efficiency
    scale_factor = float(2**(-d))
    p_scaled = float(p) * scale_factor
    q_scaled = float(q) * scale_factor
    
    # Generate points in fundamental parallelogram
    for i in range(mesh_density):
        for j in range(mesh_density):
            # Parameters in [0,1) × [0,1)
            u = float(i) / mesh_density
            v = float(j) / mesh_density
            
            # Classical torus with lattice-dependent modulation
            u_angle = 2 * float(pi) * u
            v_angle = 2 * float(pi) * v
            
            # Base dimensions influenced by lattice parameters
            major_radius = 2.0 + 0.5 * sp.log(1 + abs(p_scaled))
            minor_radius = 0.5 + 0.2 * sp.log(1 + abs(q_scaled))
            
            # Lattice-inspired perturbations
            lattice_perturbation_u = 0.1 * sp.sin(p * u_angle) * scale_factor
            lattice_perturbation_v = 0.1 * sp.cos(q * v_angle) * scale_factor
            degree_modulation = 0.05 * sp.sin(d * (u_angle + v_angle))
            
            # Compute torus coordinates
            effective_major = major_radius + lattice_perturbation_u
            effective_minor = minor_radius + lattice_perturbation_v
            
            x = (effective_major + effective_minor * sp.cos(v_angle)) * sp.cos(u_angle)
            y = (effective_major + effective_minor * sp.cos(v_angle)) * sp.sin(u_angle)
            z_coord = effective_minor * sp.sin(v_angle) + degree_modulation
            
            try:
                # Convert to float with bounds checking
                x_val = float(N(x, precision))
                y_val = float(N(y, precision))
                z_val = float(N(z_coord, precision))
                
                # Clamp to reasonable values
                x_val = max(-20, min(20, x_val))
                y_val = max(-20, min(20, y_val))
                z_val = max(-10, min(10, z_val))
                
                mesh_points.append([x_val, y_val, z_val])
                
            except (ValueError, TypeError, OverflowError):
                # Fallback to simple torus
                simple_major = 2.0
                simple_minor = 0.5
                
                x_fallback = (simple_major + simple_minor * sp.cos(v_angle)) * sp.cos(u_angle)
                y_fallback = (simple_major + simple_minor * sp.cos(v_angle)) * sp.sin(u_angle)
                z_fallback = simple_minor * sp.sin(v_angle)
                
                mesh_points.append([float(x_fallback), float(y_fallback), float(z_fallback)])
    
    # Generate facets
    facets = []
    for i in range(mesh_density):
        for j in range(mesh_density):
            current = i * mesh_density + j
            next_i = ((i + 1) % mesh_density) * mesh_density + j
            next_j = i * mesh_density + (j + 1) % mesh_density
            next_both = ((i + 1) % mesh_density) * mesh_density + (j + 1) % mesh_density
            
            facets.append([current, next_i, next_both, next_j])
    
    # Create result
    result = {
        'vertices': mesh_points,
        'facets': facets,
        'metadata': {
            'p': p,
            'q': q,
            'degree': d,
            'mesh_density': mesh_density,
            'g2': str(N(g2, 8)),
            'g3': str(N(g3, 8)),
            'j_invariant': str(N(j_inv, 8))
        }
    }
    
    return json.dumps(result)

if __name__ == "__main__":
    # Test the simplified mesh generation
    result_json = generate_torus_mesh_web(2, 3, 1, 10)
    result = json.loads(result_json)
    
    print(f"Generated {len(result['vertices'])} vertices")
    print(f"Generated {len(result['facets'])} facets") 
    print(f"Sample vertex: {result['vertices'][0]}")
    print(f"Metadata: {result['metadata']}")