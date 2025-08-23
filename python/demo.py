#!/usr/bin/env python3
"""
Demonstration of the PQTorus Python SymPy backend.

This script shows how to use the symbolic elliptic function capabilities
to compute invariants, evaluate Weierstrass functions, and work with 
torus embeddings.
"""

import sympy as sp
from sympy import I, N, pi, simplify, latex, pprint
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pqtorus import (
    primary_lattice,
    sublattice_Ld,
    compute_g2_for_Ld,
    compute_g3_for_Ld,
    elliptic_curve_for_Ld,
    wp_and_wpprime_primary,
    wp_and_wpprime_Ld,
    compute_projection_matrix
)
from pqtorus.invariants import j_invariant, compute_invariants_numerical


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def demonstrate_lattices():
    """Demonstrate lattice functionality."""
    print_section("Lattice Definitions")
    
    # Primary lattice
    p, q = 2, 3
    primary = primary_lattice(p, q)
    print(f"Primary lattice L_prim = ℤ{p} + ℤ({q}i)")
    print(f"  ω₁ = {primary.omega1}")
    print(f"  ω₂ = {primary.omega2}")
    print(f"  τ = ω₂/ω₁ = {primary.tau}")
    
    # Sublattices
    print(f"\nSublattices L_d:")
    for d in range(3):
        lattice = sublattice_Ld(p, q, d)
        print(f"  L_{d}: ω₁ = {lattice.omega1}, ω₂ = {lattice.omega2}")


def demonstrate_invariants():
    """Demonstrate invariant computation."""
    print_section("Elliptic Invariants (g₂, g₃)")
    
    p, q = 2, 3
    
    # Symbolic computation
    print("Symbolic computation (small n_max for display):")
    g2_sym = compute_g2_for_Ld(p, q, 0, n_max=3)
    g3_sym = compute_g3_for_Ld(p, q, 0, n_max=3)
    
    print(f"g₂ = {g2_sym}")
    print(f"g₃ = {g3_sym}")
    
    # Numerical computation with higher precision
    print(f"\nNumerical computation (n_max=10, precision=20):")
    g2_num, g3_num, disc_num, j_num = compute_invariants_numerical(
        p, q, 0, n_max=10, precision=20
    )
    
    print(f"g₂ ≈ {g2_num}")
    print(f"g₃ ≈ {g3_num}")
    print(f"Discriminant Δ = g₂³ - 27g₃² ≈ {disc_num}")
    print(f"j-invariant ≈ {j_num}")
    
    # Elliptic curve
    print(f"\nWeierstrass elliptic curve y² = 4x³ - g₂x - g₃:")
    g2, g3, discriminant = elliptic_curve_for_Ld(p, q, 0, n_max=5)
    print(f"y² = 4x³ - ({g2})x - ({g3})")


def demonstrate_weierstrass_functions():
    """Demonstrate Weierstrass function evaluation."""
    print_section("Weierstrass Elliptic Functions")
    
    p, q = 2, 3
    z = sp.Rational(1, 4) + sp.Rational(1, 6) * I
    
    print(f"Evaluation at z = {z}")
    
    # Primary lattice
    wp_prim, wpprime_prim = wp_and_wpprime_primary(p, q, z, n_max=5)
    print(f"\nPrimary lattice:")
    print(f"  ℘(z) = {wp_prim}")
    print(f"  ℘'(z) = {wpprime_prim}")
    
    # Sublattice degree 1
    wp_sub, wpprime_sub = wp_and_wpprime_Ld(p, q, z, d=1, n_max=5)
    print(f"\nSublattice L₁:")
    print(f"  ℘(z) = {wp_sub}")
    print(f"  ℘'(z) = {wpprime_sub}")
    
    # Numerical evaluation
    print(f"\nNumerical evaluation (precision=15):")
    wp_num, wpprime_num = wp_and_wpprime_primary(p, q, z, n_max=8, precision=15)
    print(f"  ℘(z) ≈ {wp_num}")
    print(f"  ℘'(z) ≈ {wpprime_num}")


def demonstrate_comparison_across_degrees():
    """Compare invariants across different sublattice degrees."""
    print_section("Comparison Across Sublattice Degrees")
    
    p, q = 2, 3
    
    print("Invariants for different degrees (numerical, n_max=8, precision=15):")
    print(f"{'Degree':<8} {'g₂':<25} {'g₃':<25} {'j-invariant':<25}")
    print("-" * 85)
    
    for d in range(3):
        g2_num, g3_num, _, j_num = compute_invariants_numerical(
            p, q, d, n_max=8, precision=15
        )
        print(f"{d:<8} {str(g2_num):<25} {str(g3_num):<25} {str(j_num):<25}")


def demonstrate_symbolic_manipulation():
    """Demonstrate symbolic manipulation capabilities."""
    print_section("Symbolic Manipulation")
    
    # Use symbolic parameters
    p, q = sp.symbols('p q', real=True, positive=True)
    
    print("Using symbolic parameters p, q:")
    print(f"Primary lattice: L = ℤp + ℤ(qi)")
    
    lattice = primary_lattice(p, q)
    print(f"τ = {lattice.tau}")
    
    # Symbolic g2 computation (very small n_max for display)
    print(f"\nSymbolic g₂ computation (n_max=2 for display):")
    g2_symbolic = compute_g2_for_Ld(p, q, 0, n_max=2)
    print(f"g₂ = {g2_symbolic}")
    
    # Simplification
    print(f"\nAfter simplification:")
    g2_simplified = simplify(g2_symbolic)
    print(f"g₂ = {g2_simplified}")


def demonstrate_precision_arithmetic():
    """Demonstrate arbitrary precision arithmetic."""
    print_section("Arbitrary Precision Arithmetic")
    
    p, q = 2, 3
    z = sp.Rational(1, 7)  # Use exact rational
    
    print(f"High-precision evaluation at z = {z}")
    
    precisions = [10, 20, 50]
    for prec in precisions:
        wp_z, wpprime_z = wp_and_wpprime_primary(p, q, z, n_max=10, precision=prec)
        print(f"\nPrecision {prec} digits:")
        print(f"  ℘(z) ≈ {wp_z}")
        print(f"  ℘'(z) ≈ {wpprime_z}")


def main():
    """Run all demonstrations."""
    print("PQTorus Python SymPy Backend Demonstration")
    print("=========================================")
    print("This demonstration shows the symbolic and arbitrary precision")
    print("capabilities for elliptic curve torus embeddings.")
    
    try:
        demonstrate_lattices()
        demonstrate_invariants()
        demonstrate_weierstrass_functions()
        demonstrate_comparison_across_degrees()
        demonstrate_symbolic_manipulation()
        demonstrate_precision_arithmetic()
        
        print_section("Summary")
        print("✓ Lattice definitions and sublattices")
        print("✓ Eisenstein series and elliptic invariants (g₂, g₃)")
        print("✓ Weierstrass elliptic functions (℘, ℘')")
        print("✓ Symbolic manipulation with arbitrary parameters")
        print("✓ Arbitrary precision numerical evaluation")
        print("✓ Comparison across different sublattice degrees")
        print("\nThe Python SymPy backend provides exact symbolic computation")
        print("and arbitrary precision evaluation for elliptic curve torus embeddings!")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()