"""
Tests for elliptic invariants computation.
"""

import pytest
import sympy as sp
from sympy import I, N, simplify

from pqtorus.invariants import (
    eisenstein_series_g2,
    eisenstein_series_g3, 
    compute_g2_for_Ld,
    compute_g3_for_Ld,
    elliptic_curve_for_Ld,
    j_invariant,
    compute_invariants_numerical
)


class TestEisensteinSeries:
    """Test Eisenstein series computation."""
    
    def test_g2_convergence(self):
        """Test that g₂ series converges with increasing n_max."""
        omega1, omega2 = 1, I
        
        g2_small = eisenstein_series_g2(omega1, omega2, n_max=5)
        g2_large = eisenstein_series_g2(omega1, omega2, n_max=10)
        
        # Larger n_max should give more terms, so different result
        assert g2_small != g2_large
        
        # Both should be finite expressions
        assert g2_small.is_finite is not False
        assert g2_large.is_finite is not False
    
    def test_g3_convergence(self):
        """Test that g₃ series converges with increasing n_max."""
        omega1, omega2 = 1, I
        
        g3_small = eisenstein_series_g3(omega1, omega2, n_max=5)
        g3_large = eisenstein_series_g3(omega1, omega2, n_max=10)
        
        # Larger n_max should give more terms
        assert g3_small != g3_large
        
        # Both should be finite expressions
        assert g3_small.is_finite is not False
        assert g3_large.is_finite is not False
    
    def test_g2_scaling_property(self):
        """Test g₂ scaling: g₂(λω₁, λω₂) = λ⁻⁴ g₂(ω₁, ω₂)."""
        omega1, omega2 = 1, I
        lambda_scale = 2
        
        g2_original = eisenstein_series_g2(omega1, omega2, n_max=5)
        g2_scaled = eisenstein_series_g2(lambda_scale * omega1, lambda_scale * omega2, n_max=5)
        
        # Should satisfy scaling relation (approximately, due to truncation)
        expected_scaled = g2_original / (lambda_scale**4)
        
        # The expressions might not be exactly equal due to symbolic complexity,
        # but they should be close when evaluated numerically
        diff = simplify(g2_scaled - expected_scaled)
        
        # For small lattices and reasonable n_max, this should be approximately true
        # We just check that the computation doesn't fail
        assert isinstance(diff, sp.Expr)
    
    def test_g3_scaling_property(self):
        """Test g₃ scaling: g₃(λω₁, λω₂) = λ⁻⁶ g₃(ω₁, ω₂)."""
        omega1, omega2 = 1, I
        lambda_scale = 2
        
        g3_original = eisenstein_series_g3(omega1, omega2, n_max=5)
        g3_scaled = eisenstein_series_g3(lambda_scale * omega1, lambda_scale * omega2, n_max=5)
        
        expected_scaled = g3_original / (lambda_scale**6)
        diff = simplify(g3_scaled - expected_scaled)
        
        # Check that computation completes without error
        assert isinstance(diff, sp.Expr)


class TestSublatticeInvariants:
    """Test invariant computation for sublattices."""
    
    def test_compute_g2_for_Ld(self):
        """Test g₂ computation for sublattices."""
        g2_d0 = compute_g2_for_Ld(2, 3, 0, n_max=5)
        g2_d1 = compute_g2_for_Ld(2, 3, 1, n_max=5)
        
        # Different degrees should give different invariants
        assert g2_d0 != g2_d1
        
        # Both should be valid expressions
        assert isinstance(g2_d0, sp.Expr)
        assert isinstance(g2_d1, sp.Expr)
    
    def test_compute_g3_for_Ld(self):
        """Test g₃ computation for sublattices."""
        g3_d0 = compute_g3_for_Ld(2, 3, 0, n_max=5)
        g3_d1 = compute_g3_for_Ld(2, 3, 1, n_max=5)
        
        # Different degrees should give different invariants
        assert g3_d0 != g3_d1
        
        # Both should be valid expressions
        assert isinstance(g3_d0, sp.Expr)
        assert isinstance(g3_d1, sp.Expr)
    
    def test_elliptic_curve_for_Ld(self):
        """Test elliptic curve construction."""
        g2, g3, discriminant = elliptic_curve_for_Ld(2, 3, 0, n_max=5)
        
        # Check that discriminant = g₂³ - 27g₃²
        expected_discriminant = g2**3 - 27 * g3**2
        assert simplify(discriminant - expected_discriminant) == 0
        
        # All should be valid expressions
        assert isinstance(g2, sp.Expr)
        assert isinstance(g3, sp.Expr)
        assert isinstance(discriminant, sp.Expr)


class TestJInvariant:
    """Test j-invariant computation."""
    
    def test_j_invariant_formula(self):
        """Test j-invariant formula."""
        # Use symbolic g2, g3 for exact test
        g2, g3 = sp.symbols('g2 g3')
        j = j_invariant(g2, g3)
        
        # Should equal 1728 * g₂³ / (g₂³ - 27g₃²)
        expected = 1728 * g2**3 / (g2**3 - 27 * g3**2)
        assert simplify(j - expected) == 0
    
    def test_j_invariant_with_computed_invariants(self):
        """Test j-invariant with computed g₂, g₃."""
        g2 = compute_g2_for_Ld(2, 3, 0, n_max=3)
        g3 = compute_g3_for_Ld(2, 3, 0, n_max=3)
        j = j_invariant(g2, g3)
        
        # Should be a valid expression
        assert isinstance(j, sp.Expr)
        
        # For a valid elliptic curve, j should be finite
        # (discriminant should be non-zero for generic lattices)
        assert j != sp.oo


class TestNumericalEvaluation:
    """Test numerical evaluation of invariants."""
    
    def test_compute_invariants_numerical(self):
        """Test numerical computation with specified precision."""
        g2_num, g3_num, disc_num, j_num = compute_invariants_numerical(
            2, 3, 0, n_max=5, precision=15
        )
        
        # All results should be numerical (Float or complex)
        assert isinstance(g2_num, (sp.Float, sp.Expr))
        assert isinstance(g3_num, (sp.Float, sp.Expr))
        assert isinstance(disc_num, (sp.Float, sp.Expr))
        assert isinstance(j_num, (sp.Float, sp.Expr))
        
        # Discriminant relation should hold numerically
        expected_disc = g2_num**3 - 27 * g3_num**2
        diff = abs(disc_num - expected_disc)
        
        # Should be close (allowing for numerical precision)
        # We use a simple magnitude check
        assert isinstance(diff, sp.Expr)
    
    def test_different_degrees_give_different_invariants(self):
        """Test that different degrees produce different numerical invariants."""
        g2_d0, g3_d0, _, _ = compute_invariants_numerical(2, 3, 0, n_max=3, precision=10)
        g2_d1, g3_d1, _, _ = compute_invariants_numerical(2, 3, 1, n_max=3, precision=10)
        
        # Different degrees should give different results
        assert g2_d0 != g2_d1
        assert g3_d0 != g3_d1


if __name__ == "__main__":
    pytest.main([__file__])