import React, { useState, useEffect } from 'react'
import { 
  Box, 
  Typography, 
  Slider, 
  Paper,
  Stack,
  Chip,
  Switch,
  FormControlLabel,
  Alert,
  LinearProgress
} from '@mui/material'
import { TorusParams } from '../App'
import { isPrime, nextPrime } from '../utils/primes'
import { pyodideManager } from '../utils/pyodide'

interface ControlPanelProps {
  params: TorusParams & { usePython?: boolean }
  setParams: (params: TorusParams & { usePython?: boolean }) => void
}

function ControlPanel({ params, setParams }: ControlPanelProps) {
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
  const handlePChange = (value: number) => {
    const prime = isPrime(value) ? value : nextPrime(value)
    setParams({ ...params, p: prime })
  }

  const handleQChange = (value: number) => {
    const prime = isPrime(value) ? value : nextPrime(value)
    setParams({ ...params, q: prime })
  }

  const handleDegreeChange = (value: number) => {
    setParams({ ...params, degree: Math.max(0, value) })
  }

  const handleTransparencyChange = (value: number) => {
    setParams({ ...params, transparency: value })
  }

  const handleMeshDensityChange = (value: number) => {
    setParams({ ...params, meshDensity: Math.max(5, Math.min(50, value)) })
  }

  const handlePythonToggle = (usePython: boolean) => {
    setParams({ ...params, usePython })
  }

  return (
    <Paper sx={{ p: 3, height: '100%', overflow: 'auto' }}>
      <Typography variant="h5" gutterBottom>
        Torus Controls
      </Typography>
      
      <Stack spacing={4}>
        {/* Python Backend Control */}
        <Box>
          <Typography variant="h6" gutterBottom>
            Backend Engine
          </Typography>
          
          {pyodideState.isLoading && (
            <Alert severity="info" sx={{ mb: 2 }}>
              <Box>
                <Typography variant="body2">Loading Python SymPy backend...</Typography>
                <LinearProgress sx={{ mt: 1 }} />
              </Box>
            </Alert>
          )}
          
          <FormControlLabel
            control={
              <Switch
                checked={params.usePython && pyodideState.isReady}
                onChange={(e) => handlePythonToggle(e.target.checked)}
                disabled={!pyodideState.isReady}
              />
            }
            label={
              <Box>
                <Typography>
                  {pyodideState.isReady ? 'Python SymPy Backend' : 'Classical Torus Mode'}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {pyodideState.isReady 
                    ? 'Exact elliptic function computation'
                    : pyodideState.isLoading 
                      ? 'Loading symbolic computation engine...'
                      : 'Simple parametric torus'
                  }
                </Typography>
              </Box>
            }
          />
          
          {params.usePython && pyodideState.isReady && (
            <Alert severity="success" sx={{ mt: 1 }}>
              Using Weierstrass ℘ functions and Eisenstein series for exact lattice embedding
            </Alert>
          )}
        </Box>
        <Box>
          <Typography variant="h6" gutterBottom>
            Prime Periods
          </Typography>
          
          <Box sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <Typography>p (First Prime):</Typography>
              <Chip 
                label={params.p} 
                color="primary" 
                variant="outlined" 
                size="small" 
              />
            </Box>
            <Slider
              value={params.p}
              onChange={(_, value) => handlePChange(value as number)}
              min={2}
              max={50}
              marks={[
                { value: 2, label: '2' },
                { value: 11, label: '11' },
                { value: 23, label: '23' },
                { value: 41, label: '41' }
              ]}
              valueLabelDisplay="auto"
            />
          </Box>

          <Box sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <Typography>q (Second Prime):</Typography>
              <Chip 
                label={params.q} 
                color="secondary" 
                variant="outlined" 
                size="small" 
              />
            </Box>
            <Slider
              value={params.q}
              onChange={(_, value) => handleQChange(value as number)}
              min={2}
              max={50}
              marks={[
                { value: 3, label: '3' },
                { value: 13, label: '13' },
                { value: 29, label: '29' },
                { value: 47, label: '47' }
              ]}
              valueLabelDisplay="auto"
            />
          </Box>
        </Box>

        <Box>
          <Typography variant="h6" gutterBottom>
            Approximation
          </Typography>
          
          <Box sx={{ mb: 2 }}>
            <Typography gutterBottom>Degree (d): {params.degree}</Typography>
            <Slider
              value={params.degree}
              onChange={(_, value) => handleDegreeChange(value as number)}
              min={0}
              max={5}
              step={1}
              marks
              valueLabelDisplay="auto"
            />
          </Box>
        </Box>

        <Box>
          <Typography variant="h6" gutterBottom>
            Visualization
          </Typography>
          
          <Box sx={{ mb: 2 }}>
            <Typography gutterBottom>
              Transparency: {(params.transparency * 100).toFixed(0)}%
            </Typography>
            <Slider
              value={params.transparency}
              onChange={(_, value) => handleTransparencyChange(value as number)}
              min={0.1}
              max={1.0}
              step={0.05}
              valueLabelDisplay="auto"
              valueLabelFormat={(value) => `${(value * 100).toFixed(0)}%`}
            />
          </Box>

          <Box sx={{ mb: 2 }}>
            <Typography gutterBottom>
              Mesh Density: {params.meshDensity}
            </Typography>
            <Slider
              value={params.meshDensity}
              onChange={(_, value) => handleMeshDensityChange(value as number)}
              min={5}
              max={50}
              step={5}
              marks={[
                { value: 10, label: 'Low' },
                { value: 20, label: 'Med' },
                { value: 40, label: 'High' }
              ]}
              valueLabelDisplay="auto"
            />
          </Box>
        </Box>
      </Stack>
    </Paper>
  )
}

export default ControlPanel