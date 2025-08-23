# PQTorus Python SymPy Backend

This is the Python SymPy backend for elliptic curve torus embeddings, providing symbolic and arbitrary precision computations.

## Overview

The Python backend complements the existing Kotlin/TypeScript implementations with:

- **Exact symbolic expressions** for ℘, ℘′, g₂, g₃
- **Arbitrary precision evaluation** (not limited to IEEE doubles)
- **Exploration of sublattices** L_d and their isogenous elliptic curves
- **Symbolic manipulation** for mathematical research and education
- **Client-side deployment** potential using Pyodide (Python compiled to WebAssembly)

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

```python
import sympy as sp
from pqtorus import (
    primary_lattice, sublattice_Ld,
    compute_g2_for_Ld, compute_g3_for_Ld,
    wp_and_wpprime_primary, wp_and_wpprime_Ld
)

# Define primary lattice L_prim = ℤp + ℤ(qi)
p, q = 2, 3
lattice = primary_lattice(p, q)
print(f"τ = {lattice.tau}")  # τ = 3*I/2

# Compute elliptic invariants
g2 = compute_g2_for_Ld(p, q, d=0, n_max=10)
g3 = compute_g3_for_Ld(p, q, d=0, n_max=10)

# Evaluate Weierstrass functions
z = sp.Rational(1, 4) + sp.Rational(1, 6) * sp.I
wp_z, wpprime_z = wp_and_wpprime_primary(p, q, z, n_max=10)

# High precision numerical evaluation
wp_num, wpprime_num = wp_and_wpprime_primary(
    p, q, z, n_max=15, precision=50
)
```

## Features

### 1. Lattice Definitions

- **Primary lattice**: L_prim = ℤp + ℤ(qi) with periods ω₁ = p, ω₂ = qi
- **Sublattices**: L_d = ℤp^(-d) + ℤ(q^(-d)i) for degree d ≥ 0
- **Alternative convention**: Support for primary = degree -1

```python
from pqtorus import primary_lattice, sublattice_Ld

# Primary lattice
primary = primary_lattice(2, 3)

# Sublattices of various degrees
L0 = sublattice_Ld(2, 3, 0)  # Same as primary
L1 = sublattice_Ld(2, 3, 1)  # Scaled by p^(-1), q^(-1)
L2 = sublattice_Ld(2, 3, 2)  # Scaled by p^(-2), q^(-2)
```

### 2. Elliptic Invariants

Compute g₂ and g₃ invariants from Eisenstein series:

```python
from pqtorus import compute_g2_for_Ld, compute_g3_for_Ld, elliptic_curve_for_Ld

# Symbolic computation
g2 = compute_g2_for_Ld(p=2, q=3, d=0, n_max=20)
g3 = compute_g3_for_Ld(p=2, q=3, d=0, n_max=20)

# Get complete elliptic curve
g2, g3, discriminant = elliptic_curve_for_Ld(p=2, q=3, d=0, n_max=20)
# Weierstrass form: y² = 4x³ - g₂x - g₃
```

### 3. Weierstrass Functions

Evaluate ℘(z) and ℘'(z) with arbitrary precision:

```python
from pqtorus import wp_and_wpprime_primary, wp_and_wpprime_Ld

z = sp.Rational(1, 4) + sp.I * sp.Rational(1, 6)

# On primary lattice
wp_z, wpprime_z = wp_and_wpprime_primary(p=2, q=3, z=z, n_max=15)

# On sublattice L_d
wp_z, wpprime_z = wp_and_wpprime_Ld(p=2, q=3, z=z, d=1, n_max=15)

# High precision numerical evaluation
wp_num, wpprime_num = wp_and_wpprime_primary(
    p=2, q=3, z=z, n_max=20, precision=100  # 100 decimal digits
)
```

### 4. Symbolic Manipulation

Work with symbolic parameters for research:

```python
import sympy as sp
from pqtorus import primary_lattice, compute_g2_for_Ld

# Symbolic parameters
p, q = sp.symbols('p q', real=True, positive=True)

# Symbolic lattice
lattice = primary_lattice(p, q)
print(f"τ = {lattice.tau}")  # τ = q*I/p

# Symbolic invariants
g2_symbolic = compute_g2_for_Ld(p, q, d=0, n_max=5)
g2_simplified = sp.simplify(g2_symbolic)
```

### 5. Projection Embeddings

Build projection matrices for 3D visualization:

```python
from pqtorus.projection import compute_projection_matrix, embed_torus_point

lattice = primary_lattice(2, 3)
z0 = lattice.omega1 / 4 + lattice.omega2 / 4  # Basepoint

# Compute projection matrix
projection = compute_projection_matrix(z0, lattice, n_max=10)

# Embed a point
z = sp.Rational(1, 8) + sp.I * sp.Rational(1, 12)
point_3d = embed_torus_point(z, projection, lattice, n_max=10)
```

## Mathematical Background

### Lattices

The torus T is defined as ℂ/L where:
- **Primary lattice**: L_prim = ℤp + ℤ(qi) with periods ω₁ = p, ω₂ = qi
- **Sublattices**: L_d = ℤp^(-d) + ℤ(q^(-d)i) for degree d ≥ 0

### Eisenstein Series

The elliptic invariants are computed using Eisenstein series:
- g₂ = 60 ∑_{(m,n)≠(0,0)} 1/(mω₁+nω₂)⁴
- g₃ = 140 ∑_{(m,n)≠(0,0)} 1/(mω₁+nω₂)⁶

### Weierstrass Functions

The Weierstrass ℘ function satisfies:
- ℘'(z)² = 4℘(z)³ - g₂℘(z) - g₃
- ℘''(z) = 6℘(z)² - ½g₂

### Elliptic Curves

Each lattice corresponds to an elliptic curve in Weierstrass form:
- y² = 4x³ - g₂x - g₃
- j-invariant: j = 1728g₂³/(g₂³ - 27g₃²)

## Examples

See `demo.py` for comprehensive examples demonstrating:
- Lattice constructions and sublattices
- Symbolic and numerical invariant computation
- Weierstrass function evaluation
- Arbitrary precision arithmetic
- Comparison across sublattice degrees

```bash
python demo.py
```

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest

# Run all tests
PYTHONPATH=src python -m pytest tests/ -v

# Run specific test modules
PYTHONPATH=src python -m pytest tests/test_lattice.py -v
PYTHONPATH=src python -m pytest tests/test_invariants.py -v
PYTHONPATH=src python -m pytest tests/test_elliptic.py -v
```

## API Reference

### Lattice Module (`pqtorus.lattice`)

- `Lattice(omega1, omega2)`: Create lattice with periods
- `primary_lattice(p, q)`: Create primary lattice L_prim = ℤp + ℤ(qi)
- `sublattice_Ld(p, q, d)`: Create sublattice L_d

### Invariants Module (`pqtorus.invariants`)

- `compute_g2_for_Ld(p, q, d, n_max)`: Compute g₂ for L_d
- `compute_g3_for_Ld(p, q, d, n_max)`: Compute g₃ for L_d
- `elliptic_curve_for_Ld(p, q, d, n_max)`: Get (g₂, g₃, Δ) for L_d
- `j_invariant(g2, g3)`: Compute j-invariant

### Elliptic Module (`pqtorus.elliptic`)

- `wp_and_wpprime_primary(p, q, z, n_max, precision)`: Evaluate ℘, ℘' on primary lattice
- `wp_and_wpprime_Ld(p, q, z, d, n_max, precision)`: Evaluate ℘, ℘' on L_d
- `wp_second_derivative(z, g2, g3, wp_z)`: Compute ℘''(z)

### Projection Module (`pqtorus.projection`)

- `ProjectionMatrix(matrix)`: 3×4 projection matrix class
- `compute_projection_matrix(z0, lattice, n_max)`: Compute projection at basepoint
- `embed_torus_point(z, projection, lattice, n_max, precision)`: Embed point in 3D

## Dependencies

- **SymPy** ≥ 1.12: Symbolic mathematics
- **NumPy** ≥ 1.21.0: Numerical arrays (used by SymPy)

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Code formatting
black src/ tests/
isort src/ tests/

# Linting
flake8 src/ tests/
```

## License

This project follows the same license as the main PQTorus repository.