"""
Tests for lattice definitions and operations.
"""

import pytest
import sympy as sp
from sympy import I, pi

from pqtorus.lattice import (
    Lattice, 
    primary_lattice, 
    sublattice_Ld,
    sublattice_Ld_alternative_convention,
    lattice_points_in_fundamental_domain
)


class TestLattice:
    """Test Lattice class functionality."""
    
    def test_lattice_creation(self):
        """Test basic lattice creation."""
        omega1 = sp.Integer(2)
        omega2 = sp.Integer(3) * I
        lattice = Lattice(omega1, omega2)
        
        assert lattice.omega1 == 2
        assert lattice.omega2 == 3*I
        assert lattice.periods == (2, 3*I)
    
    def test_tau_computation(self):
        """Test τ = ω₂/ω₁ computation."""
        lattice = Lattice(2, 3*I)
        expected_tau = (3*I) / 2
        assert lattice.tau == expected_tau
    
    def test_lattice_repr(self):
        """Test string representation."""
        lattice = Lattice(2, 3*I)
        repr_str = repr(lattice)
        assert "Lattice" in repr_str
        assert "ω₁=2" in repr_str
        assert "ω₂=3*I" in repr_str


class TestPrimaryLattice:
    """Test primary lattice construction."""
    
    def test_primary_lattice_integers(self):
        """Test primary lattice with integer parameters."""
        lattice = primary_lattice(2, 3)
        assert lattice.omega1 == 2
        assert lattice.omega2 == 3*I
    
    def test_primary_lattice_symbolic(self):
        """Test primary lattice with symbolic parameters."""
        p, q = sp.symbols('p q', real=True, positive=True)
        lattice = primary_lattice(p, q)
        assert lattice.omega1 == p
        assert lattice.omega2 == q*I
    
    def test_primary_lattice_tau(self):
        """Test τ computation for primary lattice."""
        lattice = primary_lattice(2, 3)
        expected_tau = (3*I) / 2
        assert lattice.tau == expected_tau


class TestSublattice:
    """Test sublattice construction."""
    
    def test_sublattice_degree_0(self):
        """Test that degree 0 gives primary lattice."""
        primary = primary_lattice(2, 3)
        sublattice = sublattice_Ld(2, 3, 0)
        
        assert sublattice.omega1 == primary.omega1
        assert sublattice.omega2 == primary.omega2
    
    def test_sublattice_degree_1(self):
        """Test degree 1 sublattice."""
        lattice = sublattice_Ld(2, 3, 1)
        assert lattice.omega1 == sp.Rational(1, 2)  # 2^(-1)
        assert lattice.omega2 == sp.Rational(1, 3) * I  # 3^(-1) * I
    
    def test_sublattice_degree_2(self):
        """Test degree 2 sublattice."""
        lattice = sublattice_Ld(2, 3, 2)
        assert lattice.omega1 == sp.Rational(1, 4)  # 2^(-2)
        assert lattice.omega2 == sp.Rational(1, 9) * I  # 3^(-2) * I
    
    def test_sublattice_negative_degree(self):
        """Test that negative degree raises error."""
        with pytest.raises(ValueError):
            sublattice_Ld(2, 3, -1)
    
    def test_sublattice_symbolic(self):
        """Test sublattice with symbolic parameters."""
        p, q = sp.symbols('p q', real=True, positive=True)
        lattice = sublattice_Ld(p, q, 1)
        assert lattice.omega1 == p**(-1)
        assert lattice.omega2 == q**(-1) * I


class TestAlternativeConvention:
    """Test alternative convention where primary = degree -1."""
    
    def test_alternative_degree_minus_1(self):
        """Test degree -1 gives primary lattice."""
        lattice = sublattice_Ld_alternative_convention(2, 3, -1)
        assert lattice.omega1 == 2
        assert lattice.omega2 == 3*I
    
    def test_alternative_degree_0(self):
        """Test degree 0 in alternative convention."""
        lattice = sublattice_Ld_alternative_convention(2, 3, 0)
        assert lattice.omega1 == sp.Rational(1, 2)  # 2^(-1)
        assert lattice.omega2 == sp.Rational(1, 3) * I  # 3^(-1) * I
    
    def test_alternative_invalid_degree(self):
        """Test invalid degree in alternative convention."""
        with pytest.raises(ValueError):
            sublattice_Ld_alternative_convention(2, 3, -2)


class TestLatticePoints:
    """Test lattice point generation."""
    
    def test_lattice_points_exclude_origin(self):
        """Test that lattice points exclude the origin."""
        lattice = Lattice(1, I)
        points = lattice_points_in_fundamental_domain(lattice, 2)
        
        # Check that origin is not included
        assert 0 not in points
    
    def test_lattice_points_count(self):
        """Test expected number of lattice points."""
        lattice = Lattice(1, I)
        points = lattice_points_in_fundamental_domain(lattice, 1)
        
        # For n_max=1, we have n1,n2 ∈ {-1,0,1}, excluding (0,0)
        # So we have 3×3 - 1 = 8 points
        assert len(points) == 8
    
    def test_lattice_points_structure(self):
        """Test structure of generated lattice points."""
        lattice = Lattice(2, 3*I)
        points = lattice_points_in_fundamental_domain(lattice, 1)
        
        # Check a few specific points
        expected_points = [
            -2 - 3*I,  # n1=-1, n2=-1
            -2,        # n1=-1, n2=0
            -2 + 3*I,  # n1=-1, n2=1
            -3*I,      # n1=0, n2=-1
            3*I,       # n1=0, n2=1
            2 - 3*I,   # n1=1, n2=-1
            2,         # n1=1, n2=0
            2 + 3*I,   # n1=1, n2=1
        ]
        
        # Convert to sets for comparison (order doesn't matter)
        assert set(points) == set(expected_points)


if __name__ == "__main__":
    pytest.main([__file__])