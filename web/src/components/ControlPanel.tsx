import React from 'react'
import { 
  Box, 
  Typography, 
  Slider, 
  Paper,
  Stack,
  Chip,
  FormControlLabel,
  Switch
} from '@mui/material'
import { TorusParams } from '../App'
import { isPrime, nextPrime } from '../utils/primes'

interface ControlPanelProps {
  params: TorusParams
  setParams: (params: TorusParams) => void
}

function ControlPanel({ params, setParams }: ControlPanelProps) {
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

  const handleWireframeToggle = (checked: boolean) => {
    setParams({ ...params, showWireframe: checked })
  }

  return (
    <Paper sx={{ p: 3, height: '100%', overflow: 'auto' }}>
      <Typography variant="h5" gutterBottom>
        Torus Controls
      </Typography>
      
      <Stack spacing={4}>
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

          <Box sx={{ mb: 2 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={params.showWireframe}
                  onChange={(e) => handleWireframeToggle(e.target.checked)}
                  color="primary"
                />
              }
              label="Show Wireframe"
            />
          </Box>
        </Box>
      </Stack>
    </Paper>
  )
}

export default ControlPanel