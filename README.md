 # Project Requirements: Interactive 3D Visualization of Elliptic Curve Tori

## Overview

This project creates an interactive 3D visualization tool for mathematical tori associated with elliptic curves, focusing on the quotient of the complex plane by a lattice defined by two prime periods. The application will use a clear separation between core logic and rendering. Core logic and math will be implemented as a self-contained library in Kotlin, compiled to WebAssembly (Wasm) for high performance and future portability.

---

## Functional Requirements

### 1. Mathematical Model (Core Logic)

- **Torus Definition**: The torus \( T \) is defined as \( \mathbb{C} / L \), where the lattice \( L := \{ n_1 p + n_2 q \mid n_1, n_2 \in \mathbb{Z} \} \), with \( p, q \) being prime numbers (fundamental periods).
- **Degree-d Approximation**: For an integer degree \( d \geq 0 \):
  - Define the sub-lattice \( L_d := \{ n_1 p^{-d} + n_2 q^{-d} \mid n_1, n_2 \in \mathbb{Z} \} \).
  - The set of vertices \( T_d \) is the projection onto \( T \) of points in \( L_d \).
  - The torus surface is approximated using quadrilateral facets whose vertices are elements of \( T_d \).
- **Kotlin-to-Wasm**: All core mathematical and lattice logic must be implemented in Kotlin, compiled to WebAssembly (Wasm) for consumption by web and (in the future) Android renderers via the SDK.

### 2. Core Logic Library (SDK)

- **Self-contained**: All math, lattice generation, torus projection, and elliptic invariants calculations must be implemented in a stand-alone, portable Kotlin library.
- **Wasm Compilation**: Library must compile to WebAssembly, exposing a stable API for use by web renderers (and, in the future, Android via a Wasm runtime).
- **API**: Provide functions for:
  - Generating lattice points and facets for given \( p, q, d \).
  - Projecting to torus surface.
  - Calculating j-invariant, discriminant, and \(\tau\).
  - Returning geometry in a format suitable for the renderer (e.g., vertices, facets, transparency).
- **Testing**: Provide unit tests for all mathematical computations.

### 3. Renderer (Web Only for MVP)

- **Web Frontend**: Use React + Three.js (via react-three-fiber) for interactive 3D visualization in the browser.
- **Renderer Layer**: The renderer must interface with the Kotlin-to-Wasm library via its public API, using the geometry and data returned for visualization.
- **Interactivity**: User can:
  - Adjust p, q (prime sliders), d (degree slider), and facet transparency.
  - Rotate, pan, and zoom 3D view.
  - View torus parameters and invariants in a status bar.

### 4. Android Renderer (Future)

- **Android Ready**: Core logic must be portable to Android by embedding a Wasm runtime or compiling to Kotlin/JVM/Native as needed.
- **API Consistency**: Maintain the same public API as for the web renderer.

### 5. GPU Acceleration and Wasm

- **WebAssembly and GPU**: Core math logic in Wasm does not use the GPU directly. GPU acceleration in the browser is enabled via WebGL/WebGPU in the renderer (e.g., Three.js), not Wasm itself.
- **Renderer Responsibility**: All heavy 3D rendering and GPU acceleration is handled by the rendering layer (Three.js/WebGL for web), not by Wasm. Wasm provides high-performance CPU-side math for geometry generation.

---

## Technical Requirements

- **Language**: Kotlin for core logic, compiled to WebAssembly (Wasm).
- **Web Renderer**: React + Three.js via react-three-fiber.
- **UI Components**: MUI or Chakra UI for controls and status bar.
- **Build Tools**: Gradle (Kotlin), npm (web), Vite or CRA for dev server.
- **Testing**: Unit tests for core logic in Kotlin, integration tests in JS/TS as needed.
- **No backend server or authentication. All logic is client-side.**

---

## Stretch Goals

- Export images/animations of the torus.
- Support for additional lattice types.
- Save/load configurations.
- Mathematical help overlay.

---

**Note:**  
- For now, only web-based rendering is required. The architecture must support future Android or other native renderers, using the same Wasm-based core logic library.
- Wasm is used for efficient, cross-platform math and geometry computations. GPU acceleration is provided by the rendering engine (Three.js/WebGL).

---
