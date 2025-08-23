"""
Lattice definitions and operations for elliptic curve torus embeddings.

Provides functionality for:
- Primary lattice L_prim = ℤp + ℤ(qi) 
- Sublattices L_d = ℤp^(-d) + ℤ(q^(-d)i) for degree d ≥ 0
- Both conventions: primary = degree -1 or primary = degree 0
"""

from typing import Tuple, Union
import sympy as sp
from sympy import I, Rational, symbols


class Lattice:
    """
    Represents a lattice in the complex plane with two periods.
    
    The lattice is defined as L = {n₁ω₁ + n₂ω₂ | n₁,n₂ ∈ ℤ}
    where ω₁, ω₂ are the fundamental periods.
    """
    
    def __init__(self, omega1: sp.Expr, omega2: sp.Expr):
        """
        Initialize lattice with two periods.
        
        Args:
            omega1: First fundamental period (complex)
            omega2: Second fundamental period (complex)
        """
        self.omega1 = omega1
        self.omega2 = omega2
        
    @property
    def tau(self) -> sp.Expr:
        """Compute τ = ω₂/ω₁ (lattice ratio)."""
        return self.omega2 / self.omega1
        
    @property 
    def periods(self) -> Tuple[sp.Expr, sp.Expr]:
        """Return the two fundamental periods."""
        return (self.omega1, self.omega2)
        
    def __repr__(self) -> str:
        return f"Lattice(ω₁={self.omega1}, ω₂={self.omega2})"


def primary_lattice(p: Union[int, sp.Expr], q: Union[int, sp.Expr]) -> Lattice:
    """
    Create the primary lattice L_prim = ℤp + ℤ(qi).
    
    Args:
        p: First prime period (real)
        q: Second prime period (real)
        
    Returns:
        Lattice with periods ω₁ = p, ω₂ = qi
    """
    omega1 = sp.sympify(p)
    omega2 = sp.sympify(q) * I
    return Lattice(omega1, omega2)


def sublattice_Ld(p: Union[int, sp.Expr], q: Union[int, sp.Expr], d: int) -> Lattice:
    """
    Create sublattice L_d = ℤp^(-d) + ℤ(q^(-d)i) for degree d ≥ 0.
    
    For d = 0, this gives the primary lattice.
    For d > 0, this gives a sublattice with scaled periods.
    
    Args:
        p: First prime period (real)
        q: Second prime period (real) 
        d: Degree (non-negative integer)
        
    Returns:
        Lattice with periods ω₁ = p^(-d), ω₂ = q^(-d)i
    """
    if d < 0:
        raise ValueError("Degree d must be non-negative")
        
    p_sym = sp.sympify(p)
    q_sym = sp.sympify(q)
    
    # For d = 0, we get the primary lattice
    # For d > 0, we scale the periods by p^(-d) and q^(-d)
    omega1 = p_sym ** (-d) if d > 0 else p_sym
    omega2 = (q_sym ** (-d)) * I if d > 0 else q_sym * I
    
    return Lattice(omega1, omega2)


def sublattice_Ld_alternative_convention(
    p: Union[int, sp.Expr], q: Union[int, sp.Expr], d: int
) -> Lattice:
    """
    Create sublattice using alternative convention where primary = degree -1.
    
    In this convention:
    - d = -1: primary lattice L_prim = ℤp + ℤ(qi)  
    - d = 0: first sublattice L_0 = ℤp^(-1) + ℤ(q^(-1)i)
    - d > 0: further sublattices L_d = ℤp^(-(d+1)) + ℤ(q^(-(d+1))i)
    
    Args:
        p: First prime period (real)
        q: Second prime period (real)
        d: Degree (integer, can be -1)
        
    Returns:
        Lattice with appropriately scaled periods
    """
    if d < -1:
        raise ValueError("Degree d must be >= -1 in alternative convention")
        
    p_sym = sp.sympify(p)
    q_sym = sp.sympify(q)
    
    if d == -1:
        # Primary lattice
        omega1 = p_sym
        omega2 = q_sym * I
    else:
        # Sublattice with degree d ≥ 0
        # Scale by p^(-(d+1)) and q^(-(d+1))
        scale_exp = -(d + 1)
        omega1 = p_sym ** scale_exp
        omega2 = (q_sym ** scale_exp) * I
        
    return Lattice(omega1, omega2)


def lattice_points_in_fundamental_domain(
    lattice: Lattice, n_max: int = 10
) -> list:
    """
    Generate lattice points in a fundamental domain for visualization.
    
    Args:
        lattice: The lattice to generate points for
        n_max: Maximum coefficient range (points with |n₁|, |n₂| ≤ n_max)
        
    Returns:
        List of complex lattice points n₁ω₁ + n₂ω₂
    """
    points = []
    for n1 in range(-n_max, n_max + 1):
        for n2 in range(-n_max, n_max + 1):
            if n1 == 0 and n2 == 0:
                continue  # Skip the origin
            point = n1 * lattice.omega1 + n2 * lattice.omega2
            points.append(point)
    return points