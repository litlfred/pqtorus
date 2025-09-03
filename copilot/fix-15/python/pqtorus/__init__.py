"""
PQTorus: Python SymPy backend for elliptic curve torus embeddings.

This package provides symbolic and arbitrary precision computations for:
- Lattice definitions and sublattice operations  
- Eisenstein series and elliptic invariants (g₂, g₃)
- Weierstrass elliptic functions (℘, ℘′)
- Projection embeddings for visualization

The implementation complements existing numeric Kotlin/TypeScript backends
with exact symbolic manipulation capabilities.
"""

from .lattice import Lattice, primary_lattice, sublattice_Ld
from .invariants import compute_g2_for_Ld, compute_g3_for_Ld, elliptic_curve_for_Ld
from .elliptic import wp_and_wpprime_primary, wp_and_wpprime_Ld
from .projection import ProjectionMatrix, compute_projection_matrix, generate_torus_mesh

__version__ = "0.1.0"
__all__ = [
    "Lattice",
    "primary_lattice", 
    "sublattice_Ld",
    "compute_g2_for_Ld",
    "compute_g3_for_Ld", 
    "elliptic_curve_for_Ld",
    "wp_and_wpprime_primary",
    "wp_and_wpprime_Ld",
    "ProjectionMatrix",
    "compute_projection_matrix",
    "generate_torus_mesh",
]