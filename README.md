 # PQTorus: Interactive 3D Visualization of Elliptic Curve Tori

## Overview

This project provides an interactive 3D visualization tool for mathematical tori associated with elliptic curves, focusing on the quotient of the complex plane by a lattice defined by two prime periods. The current implementation features a complete web-based MVP with React and Three.js for real-time 3D visualization.

## Deployment Instructions

### Prerequisites

- **Node.js**: Version 16 or higher (tested with v20.19.4)
- **npm**: Version 8 or higher (tested with v10.8.2)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/litlfred/pqtorus.git
   cd pqtorus
   ```

2. **Install dependencies:**
   ```bash
   cd web
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   
   The application will be available at `http://localhost:3000`

### Production Deployment

1. **Build for production:**
   ```bash
   cd web
   npm run build
   ```
   
   This creates optimized static files in the `dist/` directory.

2. **Preview production build locally:**
   ```bash
   npm run preview
   ```
   
   The production build will be served at `http://localhost:4173`

3. **Deploy static files:**
   
   The `dist/` directory contains all files needed for deployment. You can:
   
   - **Static hosting** (Netlify, Vercel, GitHub Pages): Upload the `dist/` folder contents
   - **Web server** (Apache, Nginx): Copy `dist/` contents to your web root
   - **CDN**: Upload files to your CDN of choice

### Deployment Examples

#### Netlify
```bash
cd web
npm run build
# Drag and drop the dist/ folder to Netlify Deploy
```

#### GitHub Pages
```bash
cd web
npm run build
# Copy dist/ contents to your gh-pages branch
```

#### Docker (Optional)
```dockerfile
FROM nginx:alpine
COPY web/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Features

- **Interactive 3D Torus Visualization**: Real-time WebGL rendering with Three.js
- **Prime Parameter Controls**: Automatic validation and adjustment of prime numbers p and q
- **Mathematical Calculations**: Live computation of τ (tau), j-invariant, and discriminant
- **Visualization Settings**: Transparency, mesh density, and degree approximation controls
- **Responsive Interface**: Material-UI components with professional styling

## Project Architecture (Future Goals)

The current MVP implements the mathematical computations directly in TypeScript for rapid prototyping. The ultimate goal is to migrate to a Kotlin-based architecture with WebAssembly for cross-platform compatibility.

### Mathematical Model

The torus T is defined as ℂ/L, where the lattice L := {n₁p + n₂q | n₁,n₂ ∈ ℤ} with prime periods p,q. 

**Current Implementation:**
- **TypeScript Mathematics**: Complex number arithmetic, lattice generation, and torus projection
- **Real-time Visualization**: WebGL rendering with Three.js and react-three-fiber
- **Interactive Controls**: Prime validation, degree approximation (d: 0-5), transparency, and mesh density
- **Live Calculations**: τ (lattice ratio), j-invariant, and discriminant computation

**Degree-d Approximation:** 
For integer degree d ≥ 0, the sub-lattice L_d := {n₁p^(-d) + n₂q^(-d) | n₁,n₂ ∈ ℤ} is used, with vertices T_d projected onto T using quadrilateral facets.

## Development

### Running Tests
```bash
cd web
npm test  # (when test suite is added)
```

### Code Structure
```
web/
├── src/
│   ├── components/         # React components
│   ├── utils/             # Mathematical utilities
│   ├── types/             # TypeScript type definitions
│   └── App.tsx            # Main application
├── package.json           # Dependencies and scripts
└── vite.config.ts         # Build configuration
```

## Future Architecture Goals

**Phase 2: Kotlin + WebAssembly**
- Migrate mathematical core to Kotlin for type safety and performance
- Compile to WebAssembly for web deployment
- Maintain same renderer interface for seamless transition
- Add comprehensive test suite for mathematical computations

**Phase 3: Cross-Platform**
- Android renderer using same Kotlin core
- Native performance optimizations
- Consistent API across platforms

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes in the `web/` directory
4. Test the build: `npm run build`
5. Submit a pull request

## License

This project is open source. Please see the license file for details.
