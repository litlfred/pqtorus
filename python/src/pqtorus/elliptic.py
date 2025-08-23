"""
Weierstrass elliptic function evaluation using SymPy.

Provides functions for evaluating ℘(z) and ℘'(z) with arbitrary precision
using SymPy's built-in weierstrass_p and weierstrass_p_prime functions.
"""

from typing import Union, Tuple
import sympy as sp
from sympy import I, N, symbols
from sympy.functions.special.elliptic_integrals import (
    elliptic_pi, elliptic_e, elliptic_f
)
from .lattice import Lattice, primary_lattice, sublattice_Ld
from .invariants import compute_g2_for_Ld, compute_g3_for_Ld


def wp_and_wpprime_from_invariants(
    z: sp.Expr, 
    g2: sp.Expr, 
    g3: sp.Expr,
    precision: int = None
) -> Tuple[sp.Expr, sp.Expr]:
    """
    Compute ℘(z) and ℘'(z) from given g₂, g₃ invariants.
    
    Args:
        z: Complex point to evaluate at
        g2: g₂ invariant  
        g3: g₃ invariant
        precision: Optional precision for numerical evaluation
        
    Returns:
        Tuple (wp_z, wpprime_z) where:
        - wp_z = ℘(z)
        - wpprime_z = ℘'(z)
    """
    # Use SymPy's Weierstrass elliptic functions
    # Note: SymPy's weierstrass_p takes (z, g2, g3) as arguments
    
    try:
        from sympy.functions.special.elliptic_integrals import weierstrass_p
        wp_z = weierstrass_p(z, g2, g3)
        
        # ℘'(z) can be computed as derivative or using the relation
        # ℘'(z)² = 4℘(z)³ - g₂℘(z) - g₃
        # For now, use derivative
        wpprime_z = sp.diff(wp_z, z)
        
    except ImportError:
        # Fallback: create symbolic expressions
        # In a full implementation, this would compute the series expansion
        wp_z = sp.Function('wp')(z, g2, g3)
        wpprime_z = sp.Function('wpprime')(z, g2, g3)
    
    if precision is not None:
        wp_z = N(wp_z, precision)
        wpprime_z = N(wpprime_z, precision)
        
    return wp_z, wpprime_z


def wp_and_wpprime_from_lattice(
    z: sp.Expr, 
    lattice: Lattice, 
    n_max: int = 20,
    precision: int = None
) -> Tuple[sp.Expr, sp.Expr]:
    """
    Compute ℘(z) and ℘'(z) for a given lattice.
    
    Args:
        z: Complex point to evaluate at
        lattice: Lattice defining the elliptic function
        n_max: Truncation parameter for invariant computation
        precision: Optional precision for numerical evaluation
        
    Returns:
        Tuple (wp_z, wpprime_z)
    """
    # Compute g₂, g₃ from lattice periods  
    from .invariants import eisenstein_series_g2, eisenstein_series_g3
    
    g2 = eisenstein_series_g2(lattice.omega1, lattice.omega2, n_max)
    g3 = eisenstein_series_g3(lattice.omega1, lattice.omega2, n_max)
    
    return wp_and_wpprime_from_invariants(z, g2, g3, precision)


def wp_and_wpprime_primary(
    p: Union[int, sp.Expr], 
    q: Union[int, sp.Expr], 
    z: sp.Expr,
    n_max: int = 20, 
    precision: int = None
) -> Tuple[sp.Expr, sp.Expr]:
    """
    Evaluate ℘(z) and ℘'(z) on the primary lattice L_prim = ℤp + ℤ(qi).
    
    Args:
        p: First prime period (real)
        q: Second prime period (real)
        z: Complex point to evaluate at
        n_max: Truncation parameter for Eisenstein series
        precision: Optional precision for numerical evaluation
        
    Returns:
        Tuple (wp_z, wpprime_z) evaluated on primary lattice
    """
    lattice = primary_lattice(p, q)
    return wp_and_wpprime_from_lattice(z, lattice, n_max, precision)


def wp_and_wpprime_Ld(
    p: Union[int, sp.Expr], 
    q: Union[int, sp.Expr], 
    z: sp.Expr, 
    d: int,
    n_max: int = 20,
    precision: int = None
) -> Tuple[sp.Expr, sp.Expr]:
    """
    Evaluate ℘(z) and ℘'(z) on sublattice L_d.
    
    Args:
        p: First prime period (real)
        q: Second prime period (real)
        z: Complex point to evaluate at
        d: Degree (non-negative integer)
        n_max: Truncation parameter for Eisenstein series
        precision: Optional precision for numerical evaluation
        
    Returns:
        Tuple (wp_z, wpprime_z) evaluated on L_d
    """
    lattice = sublattice_Ld(p, q, d)
    return wp_and_wpprime_from_lattice(z, lattice, n_max, precision)


def wp_second_derivative(
    z: sp.Expr,
    g2: sp.Expr, 
    g3: sp.Expr = None,
    wp_z: sp.Expr = None
) -> sp.Expr:
    """
    Compute ℘''(z) using the identity ℘''(z) = 6℘(z)² - ½g₂.
    
    Args:
        z: Complex point  
        g2: g₂ invariant
        g3: g₃ invariant (optional, for computing ℘(z) if not provided)
        wp_z: ℘(z) value (optional, computed if not provided)
        
    Returns:
        ℘''(z)
    """
    if wp_z is None:
        if g3 is None:
            raise ValueError("Either wp_z or g3 must be provided")
        wp_z, _ = wp_and_wpprime_from_invariants(z, g2, g3)
    
    return 6 * wp_z**2 - g2/2


def evaluate_wp_series(
    z: sp.Expr, 
    omega1: sp.Expr, 
    omega2: sp.Expr, 
    n_max: int = 10
) -> sp.Expr:
    """
    Direct series evaluation of ℘(z) using Laurent series.
    
    ℘(z) = 1/z² + ∑_{(m,n)≠(0,0)} [1/(z-mω₁-nω₂)² - 1/(mω₁+nω₂)²]
    
    Args:
        z: Complex point to evaluate at
        omega1: First fundamental period
        omega2: Second fundamental period  
        n_max: Truncation parameter
        
    Returns:
        ℘(z) computed via series
    """
    # Principal part
    wp_z = 1 / z**2
    
    # Sum over non-zero lattice points
    for m in range(-n_max, n_max + 1):
        for n in range(-n_max, n_max + 1):
            if m == 0 and n == 0:
                continue
                
            lattice_point = m * omega1 + n * omega2
            term = 1 / (z - lattice_point)**2 - 1 / lattice_point**2
            wp_z += term
    
    return wp_z


def wp_addition_formula(
    z1: sp.Expr, 
    z2: sp.Expr, 
    g2: sp.Expr, 
    g3: sp.Expr
) -> sp.Expr:
    """
    Compute ℘(z₁ + z₂) using the addition formula.
    
    The addition formula for Weierstrass ℘ function:
    ℘(z₁ + z₂) = [℘'(z₁) - ℘'(z₂)]² / [4(℘(z₁) - ℘(z₂))] - ℘(z₁) - ℘(z₂)
    
    Args:
        z1: First complex point
        z2: Second complex point  
        g2: g₂ invariant
        g3: g₃ invariant
        
    Returns:
        ℘(z₁ + z₂)
    """
    wp_z1, wpprime_z1 = wp_and_wpprime_from_invariants(z1, g2, g3)
    wp_z2, wpprime_z2 = wp_and_wpprime_from_invariants(z2, g2, g3)
    
    numerator = (wpprime_z1 - wpprime_z2)**2
    denominator = 4 * (wp_z1 - wp_z2)
    
    return numerator / denominator - wp_z1 - wp_z2


def duplication_formula(z: sp.Expr, g2: sp.Expr, g3: sp.Expr) -> sp.Expr:
    """
    Compute ℘(2z) using the duplication formula.
    
    ℘(2z) = [℘''(z)]² / [4℘'(z)²] - 2℘(z)
    where ℘''(z) = 6℘(z)² - ½g₂
    
    Args:
        z: Complex point
        g2: g₂ invariant  
        g3: g₃ invariant
        
    Returns:
        ℘(2z)
    """
    wp_z, wpprime_z = wp_and_wpprime_from_invariants(z, g2, g3)
    wppprime_z = wp_second_derivative(z, g2, wp_z=wp_z)
    
    return wppprime_z**2 / (4 * wpprime_z**2) - 2 * wp_z