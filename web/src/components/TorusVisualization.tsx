import React, { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Grid } from '@react-three/drei'
import * as THREE from 'three'
import { TorusParams } from '../App'
import { generateTorusGeometry } from '../utils/torusGenerator'

interface TorusVisualizationProps {
  params: TorusParams
}

function TorusMesh({ params }: { params: TorusParams }) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  const geometry = useMemo(() => {
    const torusData = generateTorusGeometry(params.p, params.q, params.degree, params.meshDensity)
    
    const vertices = new Float32Array(torusData.vertices.length * 3)
    for (let i = 0; i < torusData.vertices.length; i++) {
      const v = torusData.vertices[i]
      vertices[i * 3] = v.x
      vertices[i * 3 + 1] = v.y
      vertices[i * 3 + 2] = v.z
    }
    
    const indices = []
    for (const facet of torusData.facets) {
      // Convert quadrilateral to two triangles
      indices.push(facet.v1, facet.v2, facet.v3)
      indices.push(facet.v1, facet.v3, facet.v4)
    }
    
    const geom = new THREE.BufferGeometry()
    geom.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
    geom.setIndex(indices)
    geom.computeVertexNormals()
    
    return geom
  }, [params.p, params.q, params.degree, params.meshDensity])

  useFrame((state) => {
    if (meshRef.current) {
      // Gentle rotation for better visualization
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.1
    }
  })

  return (
    <mesh ref={meshRef} geometry={geometry}>
      <meshStandardMaterial
        color="#4fc3f7"
        transparent
        opacity={params.transparency}
        side={THREE.DoubleSide}
        wireframe={false}
      />
    </mesh>
  )
}

function Wireframe({ params }: { params: TorusParams }) {
  const geometry = useMemo(() => {
    const torusData = generateTorusGeometry(params.p, params.q, params.degree, params.meshDensity)
    
    const vertices = new Float32Array(torusData.vertices.length * 3)
    for (let i = 0; i < torusData.vertices.length; i++) {
      const v = torusData.vertices[i]
      vertices[i * 3] = v.x
      vertices[i * 3 + 1] = v.y
      vertices[i * 3 + 2] = v.z
    }
    
    const indices = []
    for (const facet of torusData.facets) {
      // Draw edges of quadrilateral
      indices.push(facet.v1, facet.v2)
      indices.push(facet.v2, facet.v3)
      indices.push(facet.v3, facet.v4)
      indices.push(facet.v4, facet.v1)
    }
    
    const geom = new THREE.BufferGeometry()
    geom.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
    geom.setIndex(indices)
    
    return geom
  }, [params.p, params.q, params.degree, params.meshDensity])

  // Wireframe opacity scales with transparency parameter but remains more subtle
  const wireframeOpacity = params.transparency * 0.4

  return (
    <lineSegments geometry={geometry}>
      <lineBasicMaterial color="#ffffff" opacity={wireframeOpacity} transparent />
    </lineSegments>
  )
}

function TorusVisualization({ params }: TorusVisualizationProps) {
  return (
    <Canvas camera={{ position: [5, 5, 5], fov: 60 }}>
      <ambientLight intensity={0.4} />
      <pointLight position={[10, 10, 10]} intensity={1} />
      <pointLight position={[-10, -10, -10]} intensity={0.5} />
      
      {/* Solid torus mesh - primary visualization that responds to all parameters */}
      <TorusMesh params={params} />
      
      {/* Wireframe overlay - shows mesh structure, opacity scales with transparency */}
      {params.showWireframe && <Wireframe params={params} />}
      
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
  )
}

export default TorusVisualization