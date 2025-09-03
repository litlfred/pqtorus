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