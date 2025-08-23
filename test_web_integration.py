#!/usr/bin/env python3
"""
Test script to verify the Python backend generates proper mesh data
that can be used in the web application.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python', 'src'))

from pqtorus.projection import generate_torus_mesh
from pqtorus import (
    sublattice_Ld,
    compute_g2_for_Ld,
    compute_g3_for_Ld
)
import sympy as sp
from sympy import N
import json

def test_mesh_generation():
    """Test mesh generation for web integration"""
    print("Testing Python mesh generation for web integration...")
    
    # Test parameters
    p, q, d = 2, 3, 1
    mesh_density = 10
    
    print(f"Generating mesh for p={p}, q={q}, d={d}, density={mesh_density}")
    
    try:
        # Generate the mesh
        mesh_points = generate_torus_mesh(p, q, d, mesh_density, n_max=8, precision=15)
        
        print(f"Generated {len(mesh_points)} mesh points")
        
        # Convert to web-friendly format
        vertices = []
        for point in mesh_points:
            if hasattr(point, 'evalf'):
                x = float(N(point[0], 15))
                y = float(N(point[1], 15))
                z = float(N(point[2], 15))
            else:
                x, y, z = float(point[0]), float(point[1]), float(point[2])
            
            vertices.append([x, y, z])
        
        # Generate facets
        facets = []
        for i in range(mesh_density):
            for j in range(mesh_density):
                current = i * mesh_density + j
                next_i = ((i + 1) % mesh_density) * mesh_density + j
                next_j = i * mesh_density + (j + 1) % mesh_density
                next_both = ((i + 1) % mesh_density) * mesh_density + (j + 1) % mesh_density
                
                facets.append([current, next_i, next_both, next_j])
        
        # Compute invariants
        g2 = compute_g2_for_Ld(p, q, d, n_max=8)
        g3 = compute_g3_for_Ld(p, q, d, n_max=8)
        discriminant = g2**3 - 27 * g3**2
        j_inv = 1728 * g2**3 / discriminant if discriminant != 0 else sp.oo
        
        # Create result structure matching web interface
        result = {
            'vertices': vertices,
            'facets': facets,
            'metadata': {
                'p': p,
                'q': q,
                'degree': d,
                'mesh_density': mesh_density,
                'g2': str(N(g2, 10)),
                'g3': str(N(g3, 10)),
                'j_invariant': str(N(j_inv, 10))
            }
        }
        
        print(f"Sample vertex: {vertices[0]}")
        print(f"Sample facet: {facets[0]}")
        print(f"g2 = {result['metadata']['g2']}")
        print(f"g3 = {result['metadata']['g3']}")
        print(f"j-invariant = {result['metadata']['j_invariant']}")
        
        # Write to JSON file for verification
        with open('/tmp/mesh_test.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"✓ Mesh generation successful! Output saved to /tmp/mesh_test.json")
        return True
        
    except Exception as e:
        print(f"✗ Error in mesh generation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_invariants():
    """Test invariant computation"""
    print("\nTesting invariant computation...")
    
    p, q = 2, 3
    for d in range(3):
        try:
            g2 = compute_g2_for_Ld(p, q, d, n_max=5)
            g3 = compute_g3_for_Ld(p, q, d, n_max=5)
            
            print(f"L_{d}: g2 = {N(g2, 8)}, g3 = {N(g3, 8)}")
            
        except Exception as e:
            print(f"✗ Error computing invariants for d={d}: {e}")
            return False
    
    print("✓ Invariant computation successful!")
    return True

if __name__ == "__main__":
    print("PQTorus Python Backend - Web Integration Test")
    print("=" * 50)
    
    success = True
    success &= test_invariants() 
    success &= test_mesh_generation()
    
    if success:
        print("\n🎉 All tests passed! Python backend is ready for web integration.")
    else:
        print("\n❌ Some tests failed. Check the error messages above.")
    
    sys.exit(0 if success else 1)