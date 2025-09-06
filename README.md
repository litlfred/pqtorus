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

**Automated Branch Previews** (Recommended)

Every branch automatically gets deployed to a preview URL:
- **Main branch**: `https://litlfred.github.io/pqtorus/main/`
- **Feature branches**: `https://litlfred.github.io/pqtorus/<branch-name>/`

Previews are automatically updated on every commit. No manual deployment needed!

**Manual Deployment**
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

The torus T is defined as ℂ/L, where the lattice L := {n₁p + n₂qi | n₁,n₂ ∈ ℤ} with prime periods p,q. 

**Current Implementation:**
- **TypeScript Mathematics**: Complex number arithmetic, lattice generation, and torus projection
- **Real-time Visualization**: WebGL rendering with Three.js and react-three-fiber
- **Interactive Controls**: Prime validation, degree approximation (d: 0-5), transparency, and mesh density
- **Live Calculations**: τ (lattice ratio), j-invariant, and discriminant computation

**Key Mathematical Formulas:**
- **Lattice**: L = {n₁p + n₂qi | n₁,n₂ ∈ ℤ} 
- **Tau**: τ = qi/p = i(q/p)
- **Degree-d Approximation**: L_d = {(n₁p + n₂qi)/2^d | n₁,n₂ ∈ ℤ}
- **Current j-invariant**: 1728 (placeholder)
- **Current discriminant**: pqi (simplified)

**📖 [Complete Mathematical Documentation](./MATHEMATICAL_FORMULAS.md)**

**Degree-d Approximation:** 
For integer degree d ≥ 0, the sub-lattice L_d := {n₁p*2^(-d) + n₂qi*2^(-d) | n₁,n₂ ∈ ℤ} is used, with vertices T_d projected onto T using quadrilateral facets.

## Development

### Mathematical Documentation

For detailed documentation of all mathematical formulas used in the project, see:
**📖 [Mathematical Formulas Documentation](./MATHEMATICAL_FORMULAS.md)**

This includes:
- Lattice generation formulas in terms of p and q
- Elliptic curve invariants (τ, j-invariant, discriminant)
- Degree-d approximation formulas  
- Torus projection equations
- Current vs. proper mathematical implementations

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

**Automated Branch Previews**: Every branch you push gets automatically deployed to `https://litlfred.github.io/pqtorus/<branch-name>/` for easy testing and review. Pull requests automatically receive comments with clickable preview links!

## Maintainer Instructions

### Automated Deployment System

The repository uses GitHub Actions to automatically deploy branch previews:

- **Triggers**: 
  - Every commit to any branch (except `gh-pages`)
  - Pull request events (opened, synchronized, reopened)
  - Manual dispatch from GitHub Actions UI
- **Build**: Runs `cd web && npm ci && npm run build`
- **Deploy**: Copies build output to `gh-pages` branch under `/<branch-name>/`
- **Preview URLs**: Available at `https://litlfred.github.io/pqtorus/<branch-name>/`
- **PR Integration**: Automatically comments on pull requests with clickable preview links

### Manual Deployment

You can manually trigger a deployment for any branch:

1. Go to the **Actions** tab in GitHub
2. Select the **Deploy Branch Preview** workflow
3. Click **Run workflow**
4. Choose the branch you want to deploy
5. Click **Run workflow**

The deployment will be available at `https://litlfred.github.io/pqtorus/<branch-name>/`

### Managing Deployments

- **No manual intervention needed** - deployments happen automatically
- **Each branch gets its own subdirectory** - deployments don't interfere with each other
- **Old content is overwritten** - each deployment replaces the previous version for that branch
- **gh-pages branch is auto-created** if it doesn't exist
- **PR comments are updated automatically** - existing deployment comments are updated instead of creating new ones

### Troubleshooting Deployment Issues

If deployments fail:
1. Check the Actions tab in GitHub for error logs
2. Ensure the build succeeds locally: `cd web && npm run build`
3. Verify the workflow has proper permissions (should be automatic)
4. For PR comment issues, check that the repository has "Write" permissions for pull requests

**Note**: Pull request comments may take a few moments to appear after the deployment completes.

## License

This project is open source. Please see the license file for details.
