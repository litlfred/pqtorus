# Pyodide Integration for PQTorus

This document describes the Pyodide integration that enables the Python SymPy backend to run directly in the browser.

## Overview

The web application now includes Pyodide integration to run Python code client-side, enabling:

- **Exact symbolic computation** using SymPy for elliptic invariants
- **Elliptic function-based mesh generation** using Weierstrass ℘ functions  
- **Browser-native computation** without requiring a Python server
- **Automatic fallback** to classical torus when Python isn't available

## Architecture

### Components

1. **PyodideManager** (`src/utils/pyodide.ts`)
   - Singleton manager for loading and interfacing with Pyodide
   - Loads Python dependencies (SymPy, NumPy)
   - Executes Python mesh generation functions
   - Handles errors and provides fallbacks

2. **Python Source** (`public/python/`)
   - `pqtorus_web_simple.py`: Optimized Python implementation for browser
   - Simplified elliptic function computations
   - JSON-serializable mesh data output

3. **Enhanced UI Components**
   - Python/Classical mode toggle in ControlPanel
   - Loading indicators for Pyodide initialization
   - Status display showing which backend is active
   - Enhanced StatusBar with symbolic computation results

## Features

### Symbolic Computation
- Exact Eisenstein series computation: g₂ = 60∑1/(mω₁+nω₂)⁴
- j-invariant calculation: j = 1728·g₂³/(g₂³-27g₃²)  
- Lattice-based mesh generation using elliptic functions
- Arbitrary precision arithmetic capabilities

### User Experience
- **Automatic initialization**: Pyodide loads in background on app start
- **Progressive enhancement**: Works with classical mode while Python loads
- **Visual feedback**: Loading states and backend status indicators
- **Graceful degradation**: Falls back to classical torus if Python fails

### Performance Optimizations
- **Lazy loading**: Pyodide only loads when needed
- **Efficient Python code**: Optimized algorithms for browser execution
- **Reasonable mesh densities**: Balanced between quality and performance
- **Error handling**: Robust fallbacks prevent application crashes

## Implementation Details

### Mesh Generation Process

1. **Parameters**: p (prime), q (prime), d (degree), mesh_density
2. **Lattice creation**: L_d = ℤ(p·2^(-d)) + ℤ(q·2^(-d)·i)
3. **Invariant computation**: Calculate g₂, g₃ using Eisenstein series
4. **Point generation**: Sample fundamental parallelogram
5. **Elliptic evaluation**: Compute ℘(z) and ℘'(z) at each point
6. **3D embedding**: Map complex values to (x,y,z) coordinates
7. **Facet generation**: Create quadrilateral mesh topology

### Data Flow

```
React UI → PyodideManager → Python Functions → JSON Result → Three.js Mesh
```

### Error Handling

- **Pyodide load failure**: Falls back to classical mode
- **Python execution error**: Returns simplified mesh
- **Computation timeout**: Uses approximation algorithms
- **Invalid parameters**: Validates and corrects inputs

## Browser Compatibility

- **Modern browsers**: Full Pyodide support (Chrome 57+, Firefox 52+, Safari 11+)
- **Older browsers**: Automatic fallback to classical mode
- **Mobile devices**: Works but may be slower due to computation overhead
- **Memory usage**: ~50MB additional for Pyodide runtime

## Development

### Testing the Integration

```bash
# Build and test
cd web
npm install
npm run build
npm run dev

# Access at http://localhost:3000
# Toggle Python mode in control panel
# Monitor browser console for Pyodide loading
```

### Debugging

- **Browser DevTools**: Check console for Pyodide loading messages
- **Network tab**: Verify Python source files are loaded
- **Performance tab**: Monitor computation times
- **Memory tab**: Check for memory leaks during mesh generation

### Customization

To modify the Python backend:

1. Edit `web/public/python/pqtorus_web_simple.py`
2. Adjust computation parameters (n_max, precision)
3. Rebuild and test in browser
4. Consider performance impact of changes

## Limitations

- **Initial load time**: Pyodide adds ~5-10 seconds to first load
- **Computation time**: Python in browser is slower than native
- **Memory usage**: Additional ~50MB for Python runtime
- **Offline support**: Requires CDN access for Pyodide files

## Future Enhancements

- **WebAssembly optimization**: Use compiled Python modules
- **Service worker caching**: Cache Pyodide for offline use  
- **Progressive loading**: Load Python features incrementally
- **Advanced visualizations**: More sophisticated elliptic function plots
- **Educational mode**: Interactive exploration of elliptic curve theory

## Mathematical Background

The integration provides access to the full mathematical framework:

- **Lattices**: Primary and sublattices with exact symbolic representation
- **Eisenstein series**: g₂, g₃ computed with arbitrary precision
- **Weierstrass functions**: ℘(z), ℘'(z) with series expansions
- **Elliptic curves**: y² = 4x³ - g₂x - g₃ in Weierstrass form
- **j-invariant**: Modular invariant for elliptic curve classification

This enables exact computation of torus embeddings based on rigorous elliptic function theory, going beyond simple parametric surfaces to true mathematical lattice structures.