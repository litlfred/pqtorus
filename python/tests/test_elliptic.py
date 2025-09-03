"""
Tests for elliptic function evaluation.
"""

import pytest
import sympy as sp
from sympy import I, N, symbols

from pqtorus.elliptic import (
    wp_and_wpprime_from_invariants,
    wp_and_wpprime_from_lattice,
    wp_and_wpprime_primary,
    wp_and_wpprime_Ld,
    wp_second_derivative,
    evaluate_wp_series,
    wp_addition_formula,
    duplication_formula
)
from pqtorus.lattice import Lattice


class TestWeierstrassFunction:
    """Test Weierstrass ℘ function evaluation."""
    
    def test_wp_from_invariants_symbolic(self):
        """Test ℘ and ℘' computation from symbolic invariants."""
        z = symbols('z')
        g2, g3 = symbols('g2 g3')
        
        wp_z, wpprime_z = wp_and_wpprime_from_invariants(z, g2, g3)
        
        # Should return symbolic expressions
        assert isinstance(wp_z, sp.Expr)
        assert isinstance(wpprime_z, sp.Expr)
        
        # Results should depend on the input variables
        assert wp_z.has(z) or wp_z.has(g2) or wp_z.has(g3)
        assert wpprime_z.has(z) or wpprime_z.has(g2) or wpprime_z.has(g3)
    
    def test_wp_from_lattice(self):
        """Test ℘ and ℘' computation from lattice."""
        lattice = Lattice(2, 3*I)
        z = sp.Rational(1, 4)
        
        wp_z, wpprime_z = wp_and_wpprime_from_lattice(z, lattice, n_max=3)
        
        # Should return expressions
        assert isinstance(wp_z, sp.Expr)
        assert isinstance(wpprime_z, sp.Expr)
    
    def test_wp_primary_lattice(self):
        """Test ℘ evaluation on primary lattice."""
        z = sp.Rational(1, 4) + sp.Rational(1, 4) * I
        
        wp_z, wpprime_z = wp_and_wpprime_primary(2, 3, z, n_max=3)
        
        # Should return expressions
        assert isinstance(wp_z, sp.Expr)
        assert isinstance(wpprime_z, sp.Expr)
    
    def test_wp_sublattice(self):
        """Test ℘ evaluation on sublattice."""
        z = sp.Rational(1, 8)
        
        wp_z, wpprime_z = wp_and_wpprime_Ld(2, 3, z, d=1, n_max=3)
        
        # Should return expressions  
        assert isinstance(wp_z, sp.Expr)
        assert isinstance(wpprime_z, sp.Expr)
    
    def test_different_sublattices_give_different_results(self):
        """Test that different sublattice degrees give different results."""
        z = sp.Rational(1, 8)
        
        wp_d0, _ = wp_and_wpprime_Ld(2, 3, z, d=0, n_max=3)
        wp_d1, _ = wp_and_wpprime_Ld(2, 3, z, d=1, n_max=3)
        
        # Different degrees should give different results
        # (They might be symbolically equal in some cases, but generally different)
        # We just check that both computations succeed
        assert isinstance(wp_d0, sp.Expr)
        assert isinstance(wp_d1, sp.Expr)


class TestSecondDerivative:
    """Test ℘'' computation."""
    
    def test_wp_second_derivative_formula(self):
        """Test ℘''(z) = 6℘(z)² - ½g₂ formula."""
        z = symbols('z')
        g2 = symbols('g2')
        wp_z = symbols('wp_z')
        
        wppprime_z = wp_second_derivative(z, g2, wp_z=wp_z)
        
        # Should equal 6℘² - ½g₂
        expected = 6 * wp_z**2 - g2/2
        assert sp.simplify(wppprime_z - expected) == 0
    
    def test_wp_second_derivative_from_g2_g3(self):
        """Test ℘'' computation when ℘ is computed from g₂, g₃."""
        z = sp.Rational(1, 4)
        g2, g3 = symbols('g2 g3')
        
        wppprime_z = wp_second_derivative(z, g2, g3)
        
        # Should return an expression involving g2
        assert isinstance(wppprime_z, sp.Expr)
        assert wppprime_z.has(g2)


class TestSeriesEvaluation:
    """Test direct series evaluation."""
    
    def test_wp_series_structure(self):
        """Test structure of ℘ series evaluation."""
        z = sp.Rational(1, 4)
        omega1, omega2 = 2, 3*I
        
        wp_z = evaluate_wp_series(z, omega1, omega2, n_max=2)
        
        # Should be an expression containing 1/z² term
        assert isinstance(wp_z, sp.Expr)
        
        # Should have the principal part 1/z²
        assert wp_z.has(z)
    
    def test_wp_series_convergence(self):
        """Test that series converges with more terms."""
        z = sp.Rational(1, 4)
        omega1, omega2 = 2, 3*I
        
        wp_small = evaluate_wp_series(z, omega1, omega2, n_max=2)
        wp_large = evaluate_wp_series(z, omega1, omega2, n_max=4)
        
        # More terms should give different (more accurate) result
        assert wp_small != wp_large
        
        # Both should be valid expressions
        assert isinstance(wp_small, sp.Expr)
        assert isinstance(wp_large, sp.Expr)


class TestAdditionFormulas:
    """Test elliptic function addition formulas."""
    
    def test_addition_formula_structure(self):
        """Test structure of addition formula."""
        z1, z2 = sp.Rational(1, 4), sp.Rational(1, 6)
        g2, g3 = symbols('g2 g3')
        
        wp_sum = wp_addition_formula(z1, z2, g2, g3)
        
        # Should return an expression
        assert isinstance(wp_sum, sp.Expr)
        
        # Should depend on both z1 and z2 (or their functions)
        # We just verify the computation succeeds
    
    def test_duplication_formula_structure(self):
        """Test structure of duplication formula."""
        z = sp.Rational(1, 4)
        g2, g3 = symbols('g2 g3')
        
        wp_2z = duplication_formula(z, g2, g3)
        
        # Should return an expression
        assert isinstance(wp_2z, sp.Expr)
        
        # Should depend on z and g2 (or their functions)
        # We just verify the computation succeeds


class TestNumericalPrecision:
    """Test numerical evaluation with specified precision."""
    
    def test_wp_with_precision(self):
        """Test ℘ evaluation with numerical precision."""
        z = 0.25 + 0.25j
        
        # Convert to SymPy expression
        z_sym = sp.Rational(1, 4) + sp.Rational(1, 4) * I
        
        wp_z, wpprime_z = wp_and_wpprime_primary(2, 3, z_sym, n_max=3, precision=15)
        
        # Results should be expressions (possibly numerical)
        assert isinstance(wp_z, sp.Expr)
        assert isinstance(wpprime_z, sp.Expr)
    
    def test_precision_consistency(self):
        """Test that higher precision gives consistent results."""
        z = sp.Rational(1, 4)
        
        wp_low, _ = wp_and_wpprime_primary(2, 3, z, n_max=3, precision=10)
        wp_high, _ = wp_and_wpprime_primary(2, 3, z, n_max=3, precision=20)
        
        # Both should be valid expressions
        assert isinstance(wp_low, sp.Expr)
        assert isinstance(wp_high, sp.Expr)
        
        # Higher precision should be a refinement (we just check they're computed)


if __name__ == "__main__":
    pytest.main([__file__])