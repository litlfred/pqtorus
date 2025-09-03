import React, { useRef, useMemo, useState, useEffect } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Grid } from '@react-three/drei'
import { Box, CircularProgress, Typography, Chip } from '@mui/material'
import * as THREE from 'three'
import { TorusParams } from '../App'
import { generateTorusGeometry } from '../utils/torusGenerator'
import { pyodideManager } from '../utils/pyodide'

interface TorusVisualizationProps {
  params: TorusParams
}

interface MeshState {
  geometry: THREE.BufferGeometry | null
  wireframeGeometry: THREE.BufferGeometry | null
  isLoading: boolean
  error: string | null
  usedPython: boolean
  metadata?: any
}

function TorusMesh({ params }: { params: TorusParams }) {
  const meshRef = useRef<THREE.Mesh>(null)
  const [meshState, setMeshState] = useState<MeshState>({
    geometry: null,
    wireframeGeometry: null,
    isLoading: false,
    error: null,
    usedPython: false
  })

  // Generate geometry when parameters change
  useEffect(() => {
    let isCancelled = false

    const generateMesh = async () => {
      setMeshState(prev => ({
        ...prev,
        isLoading: true,
        error: null
      }))

      try {
        // Try to use Python if available, fallback to classical
        const torusData = await generateTorusGeometry(
          params.p, 
          params.q, 
          params.degree, 
          params.meshDensity,
          params.usePython // Use the parameter from props
        )

        if (isCancelled) return

        // Create vertices array
        const vertices = new Float32Array(torusData.vertices.length * 3)
        for (let i = 0; i < torusData.vertices.length; i++) {
          const v = torusData.vertices[i]
          vertices[i * 3] = v.x
          vertices[i * 3 + 1] = v.y
          vertices[i * 3 + 2] = v.z
        }

        // Create triangular indices for mesh
        const meshIndices = []
        for (const facet of torusData.facets) {
          // Convert quadrilateral to two triangles
          meshIndices.push(facet.v1, facet.v2, facet.v3)
          meshIndices.push(facet.v1, facet.v3, facet.v4)
        }

        // Create wireframe indices
        const wireframeIndices = []
        for (const facet of torusData.facets) {
          // Draw edges of quadrilateral
          wireframeIndices.push(facet.v1, facet.v2)
          wireframeIndices.push(facet.v2, facet.v3)
          wireframeIndices.push(facet.v3, facet.v4)
          wireframeIndices.push(facet.v4, facet.v1)
        }

        // Create mesh geometry
        const meshGeom = new THREE.BufferGeometry()
        meshGeom.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
        meshGeom.setIndex(meshIndices)
        meshGeom.computeVertexNormals()

        // Create wireframe geometry
        const wireGeom = new THREE.BufferGeometry()
        wireGeom.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
        wireGeom.setIndex(wireframeIndices)

        setMeshState({
          geometry: meshGeom,
          wireframeGeometry: wireGeom,
          isLoading: false,
          error: null,
          usedPython: torusData.usePython || false,
          metadata: torusData.metadata
        })

      } catch (error) {
        if (!isCancelled) {
          console.error('Error generating mesh:', error)
          setMeshState(prev => ({
            ...prev,
            isLoading: false,
            error: error instanceof Error ? error.message : 'Unknown error'
          }))
        }
      }
    }

    generateMesh()

    return () => {
      isCancelled = true
    }
  }, [params.p, params.q, params.degree, params.meshDensity, params.usePython])

  useFrame((state) => {
    if (meshRef.current) {
      // Gentle rotation for better visualization
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.1
    }
  })

  if (meshState.isLoading) {
    return null // Loading will be shown in parent component
  }

  if (meshState.error || !meshState.geometry) {
    return null // Error will be shown in parent component
  }

  return (
    <>
      <mesh ref={meshRef} geometry={meshState.geometry}>
        <meshStandardMaterial
          color={meshState.usedPython ? "#4fc3f7" : "#ff9800"}
          transparent
          opacity={params.transparency}
          side={THREE.DoubleSide}
          wireframe={false}
        />
      </mesh>
      
      {meshState.wireframeGeometry && (
        <lineSegments geometry={meshState.wireframeGeometry}>
          <lineBasicMaterial 
            color="#ffffff" 
            opacity={0.3} 
            transparent 
          />
        </lineSegments>
      )}
    </>
  )
}

function Wireframe({ params }: { params: TorusParams }) {
  // Wireframe is now handled in TorusMesh component
  return null
}

function PyodideStatus() {
  const [pyodideState, setPyodideState] = useState({
    isLoading: pyodideManager.isLoadingPyodide(),
    isReady: pyodideManager.isReady()
  })

  useEffect(() => {
    const checkPyodideState = () => {
      setPyodideState({
        isLoading: pyodideManager.isLoadingPyodide(),
        isReady: pyodideManager.isReady()
      })
    }

    // Initialize Pyodide if not already done
    if (!pyodideState.isReady && !pyodideState.isLoading) {
      pyodideManager.initialize().then(checkPyodideState)
    }

    // Check state periodically during loading
    let interval: NodeJS.Timeout | null = null
    if (pyodideState.isLoading) {
      interval = setInterval(checkPyodideState, 1000)
    }

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [pyodideState.isLoading])

  if (pyodideState.isLoading) {
    return (
      <Box
        position="absolute"
        top={16}
        left={16}
        display="flex"
        alignItems="center"
        gap={1}
        sx={{ 
          backgroundColor: 'rgba(0,0,0,0.7)', 
          padding: 1, 
          borderRadius: 1,
          zIndex: 1000
        }}
      >
        <CircularProgress size={20} />
        <Typography variant="body2" color="white">
          Loading Python backend...
        </Typography>
      </Box>
    )
  }

  return (
    <Box
      position="absolute"
      top={16}
      left={16}
      sx={{ zIndex: 1000 }}
    >
      <Chip
        label={pyodideState.isReady ? "Python SymPy Active" : "Classical Mode"}
        color={pyodideState.isReady ? "success" : "default"}
        size="small"
      />
    </Box>
  )
}

function TorusVisualization({ params }: TorusVisualizationProps) {
  return (
    <Box sx={{ position: 'relative', width: '100%', height: '100%' }}>
      <PyodideStatus />
      
      <Canvas camera={{ position: [5, 5, 5], fov: 60 }}>
        <ambientLight intensity={0.4} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} />
        
        <TorusMesh params={params} />
        
        <Grid
          infiniteGrid
          sectionColor="#444444"
          sectionSize={1}
          cellColor="#222222"
          cellSize={0.2}
          fadeDistance={30}
          fadeStrength={1}
        />
        
        <OrbitControls enablePan enableZoom enableRotate />
      </Canvas>
    </Box>
  )
}

export default TorusVisualization