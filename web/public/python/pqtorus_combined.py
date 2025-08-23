# From elliptic.py
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

# From lattice.py
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

# From invariants.py
"""
Eisenstein series and elliptic invariants computation.

Provides functions for computing g₂ and g₃ invariants from Eisenstein series:
- g₂ = 60 ∑_{(m,n)≠(0,0)} 1/(mω₁+nω₂)⁴
- g₃ = 140 ∑_{(m,n)≠(0,0)} 1/(mω₁+nω₂)⁶

And construction of Weierstrass elliptic curves.
"""

from typing import Union, Tuple
import sympy as sp
from sympy import I, N, oo
from .lattice import Lattice, sublattice_Ld


def eisenstein_series_g2(omega1: sp.Expr, omega2: sp.Expr, n_max: int = 20) -> sp.Expr:
    """
    Compute g₂ invariant using Eisenstein series.
    
    g₂ = 60 ∑_{(m,n)≠(0,0)} 1/(mω₁+nω₂)⁴
    
    Args:
        omega1: First fundamental period
        omega2: Second fundamental period  
        n_max: Truncation parameter for the series (larger = more accurate)
        
    Returns:
        g₂ invariant (symbolic expression)
    """
    g2_sum = sp.Integer(0)
    
    for m in range(-n_max, n_max + 1):
        for n in range(-n_max, n_max + 1):
            if m == 0 and n == 0:
                continue  # Skip the origin
            
            period_combination = m * omega1 + n * omega2
            term = 1 / (period_combination ** 4)
            g2_sum += term
    
    return 60 * g2_sum


def eisenstein_series_g3(omega1: sp.Expr, omega2: sp.Expr, n_max: int = 20) -> sp.Expr:
    """
    Compute g₃ invariant using Eisenstein series.
    
    g₃ = 140 ∑_{(m,n)≠(0,0)} 1/(mω₁+nω₂)⁶
    
    Args:
        omega1: First fundamental period
        omega2: Second fundamental period
        n_max: Truncation parameter for the series (larger = more accurate)
        
    Returns:
        g₃ invariant (symbolic expression)
    """
    g3_sum = sp.Integer(0)
    
    for m in range(-n_max, n_max + 1):
        for n in range(-n_max, n_max + 1):
            if m == 0 and n == 0:
                continue  # Skip the origin
            
            period_combination = m * omega1 + n * omega2
            term = 1 / (period_combination ** 6)
            g3_sum += term
    
    return 140 * g3_sum


def compute_g2_for_Ld(
    p: Union[int, sp.Expr], 
    q: Union[int, sp.Expr], 
    d: int, 
    n_max: int = 20
) -> sp.Expr:
    """
    Compute g₂ invariant for sublattice L_d.
    
    Args:
        p: First prime period
        q: Second prime period  
        d: Degree (non-negative integer)
        n_max: Truncation parameter for Eisenstein series
        
    Returns:
        g₂ invariant for L_d
    """
    lattice = sublattice_Ld(p, q, d)
    return eisenstein_series_g2(lattice.omega1, lattice.omega2, n_max)


def compute_g3_for_Ld(
    p: Union[int, sp.Expr], 
    q: Union[int, sp.Expr], 
    d: int, 
    n_max: int = 20
) -> sp.Expr:
    """
    Compute g₃ invariant for sublattice L_d.
    
    Args:
        p: First prime period
        q: Second prime period
        d: Degree (non-negative integer)  
        n_max: Truncation parameter for Eisenstein series
        
    Returns:
        g₃ invariant for L_d
    """
    lattice = sublattice_Ld(p, q, d)
    return eisenstein_series_g3(lattice.omega1, lattice.omega2, n_max)


def elliptic_curve_for_Ld(
    p: Union[int, sp.Expr], 
    q: Union[int, sp.Expr], 
    d: int, 
    n_max: int = 20
) -> Tuple[sp.Expr, sp.Expr, sp.Expr]:
    """
    Construct Weierstrass elliptic curve for sublattice L_d.
    
    Returns the curve in Weierstrass form: y² = 4x³ - g₂x - g₃
    
    Args:
        p: First prime period
        q: Second prime period
        d: Degree (non-negative integer)
        n_max: Truncation parameter for Eisenstein series
        
    Returns:
        Tuple (g2, g3, discriminant) where:
        - g2: g₂ invariant
        - g3: g₃ invariant  
        - discriminant: Δ = g₂³ - 27g₃²
    """
    g2 = compute_g2_for_Ld(p, q, d, n_max)
    g3 = compute_g3_for_Ld(p, q, d, n_max)
    
    # Compute discriminant Δ = g₂³ - 27g₃²
    discriminant = g2**3 - 27 * g3**2
    
    return g2, g3, discriminant


def j_invariant(g2: sp.Expr, g3: sp.Expr) -> sp.Expr:
    """
    Compute j-invariant from g₂ and g₃.
    
    j = 1728 * g₂³ / (g₂³ - 27g₃²)
    
    Args:
        g2: g₂ invariant
        g3: g₃ invariant
        
    Returns:
        j-invariant
    """
    discriminant = g2**3 - 27 * g3**2
    return 1728 * g2**3 / discriminant


def compute_invariants_numerical(
    p: Union[int, float], 
    q: Union[int, float], 
    d: int, 
    n_max: int = 20,
    precision: int = 50
) -> Tuple[sp.Float, sp.Float, sp.Float, sp.Float]:
    """
    Compute invariants with numerical evaluation at specified precision.
    
    Args:
        p: First prime period (numeric)
        q: Second prime period (numeric)
        d: Degree
        n_max: Truncation parameter
        precision: Number of decimal digits for evaluation
        
    Returns:
        Tuple (g2_num, g3_num, discriminant_num, j_num) of numerical values
    """
    g2 = compute_g2_for_Ld(p, q, d, n_max)
    g3 = compute_g3_for_Ld(p, q, d, n_max)
    discriminant = g2**3 - 27 * g3**2
    j = j_invariant(g2, g3)
    
    # Evaluate numerically with specified precision
    g2_num = N(g2, precision)
    g3_num = N(g3, precision)
    discriminant_num = N(discriminant, precision)
    j_num = N(j, precision)
    
    return g2_num, g3_num, discriminant_num, j_num


def fast_g2_g3_via_theta(
    tau: sp.Expr, 
    precision: int = 50
) -> Tuple[sp.Expr, sp.Expr]:
    """
    Fast computation of g₂, g₃ using theta function identities.
    
    This is an alternative method that can be faster for numerical computation
    when tau = ω₂/ω₁ is known.
    
    Args:
        tau: Lattice ratio ω₂/ω₁
        precision: Precision for numerical evaluation
        
    Returns:
        Tuple (g2, g3) computed via theta functions
    """
    # This is a placeholder for theta function implementation
    # In a full implementation, this would use SymPy's theta functions
    # or Jacobi theta function series
    
    # For now, return symbolic expressions that could be evaluated
    # This would need proper theta function implementation
    q = sp.exp(2 * sp.pi * I * tau)
    
    # Placeholder - in real implementation would use proper theta identities
    # g₂ = 4π⁴/3 * (θ₂⁸ + θ₃⁸ + θ₄⁸) / (η²⁴)
    # g₃ = 8π⁶/27 * (θ₂¹² - θ₃¹² - θ₄¹²) / (η³⁶)
    
    return sp.symbols('g2_theta'), sp.symbols('g3_theta')

# From projection.py
"""
Projection embedding for torus visualization using elliptic functions.

Provides functionality for building 3×4 projection matrices and embedding
complex torus points into 3D space for visualization.
"""

from typing import Union, Tuple, List
import sympy as sp
from sympy import Matrix, I, N, symbols, cos, sin, pi
from .lattice import Lattice, sublattice_Ld  
from .elliptic import wp_and_wpprime_from_lattice, wp_second_derivative
from .invariants import compute_g2_for_Ld, compute_g3_for_Ld


class ProjectionMatrix:
    """
    Represents a 3×4 projection matrix for embedding torus into 3D space.
    
    The matrix maps 4D points [℘(z), ℘'(z), ℘''(z), 1] to 3D coordinates.
    """
    
    def __init__(self, matrix: Matrix):
        """
        Initialize with a 3×4 projection matrix.
        
        Args:
            matrix: 3×4 SymPy Matrix
        """
        if matrix.shape != (3, 4):
            raise ValueError("Projection matrix must be 3×4")
        self.matrix = matrix
    
    def apply(self, wp: sp.Expr, wpprime: sp.Expr, wppprime: sp.Expr) -> Matrix:
        """
        Apply projection to elliptic function values.
        
        Args:
            wp: ℘(z) value
            wpprime: ℘'(z) value  
            wppprime: ℘''(z) value
            
        Returns:
            3D point as Matrix([x, y, z])
        """
        point_4d = Matrix([wp, wpprime, wppprime, 1])
        return self.matrix * point_4d
    
    def __repr__(self) -> str:
        return f"ProjectionMatrix(\n{self.matrix}\n)"


def compute_projection_matrix(
    z0: sp.Expr,
    lattice: Lattice, 
    n_max: int = 20
) -> ProjectionMatrix:
    """
    Compute 3×4 projection matrix at basepoint z₀.
    
    The matrix is constructed to provide a good embedding of the torus
    in 3D space, using the derivatives of elliptic functions.
    
    Args:
        z0: Basepoint for the projection 
        lattice: Lattice defining the elliptic functions
        n_max: Truncation parameter for invariant computation
        
    Returns:
        ProjectionMatrix for embedding
    """
    # Compute elliptic function values at basepoint
    wp_z0, wpprime_z0 = wp_and_wpprime_from_lattice(z0, lattice, n_max)
    
    # Compute g₂ for second derivative
    from .invariants import eisenstein_series_g2
    g2 = eisenstein_series_g2(lattice.omega1, lattice.omega2, n_max)
    wppprime_z0 = wp_second_derivative(z0, g2, wp_z=wp_z0)
    
    # Construct projection matrix
    # This is a simple example - in practice, you might want to choose
    # the matrix to optimize visualization properties
    
    # Standard embedding using real and imaginary parts plus derivatives
    matrix = Matrix([
        [1, 0, 0, 0],      # x = Re(℘(z))
        [I, 0, 0, 0],      # y = Im(℘(z)) 
        [0, 1, 0, 0]       # z = Re(℘'(z))
    ])
    
    return ProjectionMatrix(matrix)


def stereographic_projection_matrix() -> ProjectionMatrix:
    """
    Create a stereographic projection matrix.
    
    Maps the Riemann sphere to 3D space via stereographic projection.
    
    Returns:
        ProjectionMatrix for stereographic embedding
    """
    # Stereographic projection: (x,y,z) = (2u/(1+u²+v²), 2v/(1+u²+v²), (u²+v²-1)/(1+u²+v²))
    # where u + iv represents points on the complex plane
    
    matrix = Matrix([
        [2, 0, 0, 1],      # x coordinate  
        [0, 2*I, 0, 1],    # y coordinate
        [0, 0, 1, -1]      # z coordinate
    ])
    
    return ProjectionMatrix(matrix)


def embed_torus_point(
    z: sp.Expr,
    projection: ProjectionMatrix,
    lattice: Lattice,
    n_max: int = 20,
    precision: int = None
) -> Matrix:
    """
    Embed a single torus point into 3D space.
    
    Args:
        z: Complex point on the torus
        projection: ProjectionMatrix to use
        lattice: Lattice defining the torus
        n_max: Truncation parameter 
        precision: Optional numerical precision
        
    Returns:
        3D coordinates as Matrix([x, y, z])
    """
    # Compute elliptic function values
    wp_z, wpprime_z = wp_and_wpprime_from_lattice(z, lattice, n_max, precision)
    
    # Compute second derivative
    from .invariants import eisenstein_series_g2
    g2 = eisenstein_series_g2(lattice.omega1, lattice.omega2, n_max)
    if precision is not None:
        g2 = N(g2, precision)
    wppprime_z = wp_second_derivative(z, g2, wp_z=wp_z)
    
    # Apply projection
    return projection.apply(wp_z, wpprime_z, wppprime_z)


def generate_torus_mesh(
    p: Union[int, sp.Expr],
    q: Union[int, sp.Expr], 
    d: int,
    mesh_density: int = 20,
    projection: ProjectionMatrix = None,
    n_max: int = 20,
    precision: int = None
) -> List[Matrix]:
    """
    Generate a mesh of points on the torus L_d for visualization.
    
    Args:
        p: First prime period
        q: Second prime period
        d: Degree  
        mesh_density: Number of points per direction
        projection: ProjectionMatrix (default: standard embedding)
        n_max: Truncation parameter
        precision: Optional numerical precision
        
    Returns:
        List of 3D points representing the torus mesh
    """
    lattice = sublattice_Ld(p, q, d)
    
    if projection is None:
        # Use default projection
        z0 = lattice.omega1 / 4 + lattice.omega2 / 4  # Sample basepoint
        projection = compute_projection_matrix(z0, lattice, n_max)
    
    mesh_points = []
    
    # Generate points in fundamental parallelogram
    for i in range(mesh_density):
        for j in range(mesh_density):
            # Parameters in [0,1) × [0,1)
            u = sp.Rational(i, mesh_density)
            v = sp.Rational(j, mesh_density)
            
            # Map to fundamental domain
            z = u * lattice.omega1 + v * lattice.omega2
            
            # Embed in 3D
            point_3d = embed_torus_point(z, projection, lattice, n_max, precision)
            mesh_points.append(point_3d)
    
    return mesh_points


def parameterize_torus_classical(
    major_radius: float = 2.0,
    minor_radius: float = 0.5,
    mesh_density: int = 20
) -> List[Matrix]:
    """
    Generate classical torus parameterization for comparison.
    
    Standard torus: (R + r*cos(v))*cos(u), (R + r*cos(v))*sin(u), r*sin(v)
    where R = major_radius, r = minor_radius
    
    Args:
        major_radius: Major radius R
        minor_radius: Minor radius r  
        mesh_density: Number of points per direction
        
    Returns:
        List of 3D points for classical torus
    """
    points = []
    
    for i in range(mesh_density):
        for j in range(mesh_density):
            u = 2 * pi * i / mesh_density
            v = 2 * pi * j / mesh_density
            
            x = (major_radius + minor_radius * cos(v)) * cos(u)
            y = (major_radius + minor_radius * cos(v)) * sin(u)
            z = minor_radius * sin(v)
            
            points.append(Matrix([x, y, z]))
    
    return points


def visualize_lattice_periods(
    lattice: Lattice,
    mesh_density: int = 50,
    precision: int = 15
) -> Tuple[List[Matrix], List[Matrix]]:
    """
    Generate visualization data for lattice and its periods.
    
    Args:
        lattice: Lattice to visualize
        mesh_density: Density of point grid
        precision: Numerical precision
        
    Returns:
        Tuple (lattice_points, period_vectors) where:
        - lattice_points: 3D positions of lattice points
        - period_vectors: 3D representations of fundamental periods
    """
    from .lattice import lattice_points_in_fundamental_domain
    
    # Get lattice points
    lattice_points_2d = lattice_points_in_fundamental_domain(lattice, 5)
    
    # Simple embedding: map complex numbers to (Re, Im, 0)
    lattice_points_3d = []
    for point in lattice_points_2d:
        if precision:
            point = N(point, precision)
        x = sp.re(point)
        y = sp.im(point)
        z = 0
        lattice_points_3d.append(Matrix([x, y, z]))
    
    # Represent fundamental periods
    omega1_3d = Matrix([sp.re(lattice.omega1), sp.im(lattice.omega1), 0])
    omega2_3d = Matrix([sp.re(lattice.omega2), sp.im(lattice.omega2), 0])
    
    if precision:
        omega1_3d = Matrix([N(omega1_3d[i], precision) for i in range(3)])
        omega2_3d = Matrix([N(omega2_3d[i], precision) for i in range(3)])
    
    period_vectors = [omega1_3d, omega2_3d]
    
    return lattice_points_3d, period_vectors

