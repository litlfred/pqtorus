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
    Create sublattice L_d with proper lattice periods for L_d = ℤ(p*2^(-d)) + ℤ(q*2^(-d)*i).
    
    The lattice points are L_d(m,n) = m/p^d + i*n/q^d where 0 ≤ m < p^d and 0 ≤ n < q^d.
    This corresponds to periods ω₁ = p*2^(-d), ω₂ = q*2^(-d)*i.
    
    Args:
        p: First prime period (real)
        q: Second prime period (real) 
        d: Degree (non-negative integer)
        
    Returns:
        Lattice with periods ω₁ = p*2^(-d), ω₂ = q*2^(-d)*i
    """
    if d < 0:
        raise ValueError("Degree d must be non-negative")
        
    p_sym = sp.sympify(p)
    q_sym = sp.sympify(q)
    
    # Use exact rational arithmetic for the scaling factor
    scale = sp.Rational(1, 2**d) if d > 0 else sp.Rational(1)
    
    # Lattice periods: ω₁ = p*2^(-d), ω₂ = q*2^(-d)*i
    omega1 = p_sym * scale
    omega2 = q_sym * scale * I
    
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


def generate_lattice_points_Ld(
    p: Union[int, sp.Expr], 
    q: Union[int, sp.Expr], 
    d: int, 
    max_points_per_direction: int = None
) -> list:
    """
    Generate discrete lattice points L_d(m,n) = m/p^d + i*n/q^d with exact rational arithmetic.
    
    This implements the proper L_d lattice structure where:
    - 0 ≤ m < p^d and 0 ≤ n < q^d for d > 0
    - For d = 0, uses reasonable bounds based on p, q
    
    Args:
        p: First prime period (integer)
        q: Second prime period (integer)
        d: Degree (non-negative integer)
        max_points_per_direction: Maximum points per direction (for performance)
        
    Returns:
        List of complex lattice points using exact rational arithmetic
    """
    p_int = int(p)
    q_int = int(q)
    
    if d == 0:
        # For d=0, use reasonable range for visualization
        m_max = max_points_per_direction or min(p_int, 20)
        n_max = max_points_per_direction or min(q_int, 20)
    else:
        # For d > 0, use p^d and q^d as theoretical upper bounds
        m_max = min(p_int**d, max_points_per_direction or 50)
        n_max = min(q_int**d, max_points_per_direction or 50)
    
    lattice_points = []
    for m in range(int(m_max)):
        for n in range(int(n_max)):
            # L_d(m,n) = m/p^d + i*n/q^d using exact rational arithmetic
            if d == 0:
                point = sp.Rational(m) + I * sp.Rational(n)
            else:
                point = sp.Rational(m, p_int**d) + I * sp.Rational(n, q_int**d)
            lattice_points.append(point)
    
    return lattice_points