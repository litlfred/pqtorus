import React, { useState, useEffect } from 'react'
import { Paper, Typography, Grid, Box, Chip, Accordion, AccordionSummary, AccordionDetails } from '@mui/material'
import { ExpandMore } from '@mui/icons-material'
import { TorusParams } from '../App'
import { calculateEllipticInvariants } from '../utils/ellipticMath'
import { pyodideManager } from '../utils/pyodide'

interface StatusBarProps {
  params: TorusParams
}

interface PythonInvariants {
  g2: string
  g3: string
  jInvariant: string
  usedPython: boolean
}

function StatusBar({ params }: StatusBarProps) {
  const [pythonInvariants, setPythonInvariants] = useState<PythonInvariants | null>(null)
  const invariants = calculateEllipticInvariants(params.p, params.q)
  
  // Try to get Python-computed invariants
  useEffect(() => {
    const getPythonInvariants = async () => {
      if (pyodideManager.isReady()) {
        try {
          // Generate a small mesh to get the metadata with invariants
          const result = await pyodideManager.generateTorusMesh(params.p, params.q, params.degree, 5)
          setPythonInvariants({
            g2: result.metadata.g2,
            g3: result.metadata.g3,
            jInvariant: result.metadata.jInvariant,
            usedPython: true
          })
        } catch (error) {
          console.warn('Failed to get Python invariants:', error)
          setPythonInvariants({
            g2: 'Error',
            g3: 'Error', 
            jInvariant: 'Error',
            usedPython: false
          })
        }
      }
    }
    
    getPythonInvariants()
  }, [params.p, params.q, params.degree])
  
  return (
    <Paper sx={{ borderRadius: 0 }}>
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6">
            Elliptic Curve Parameters & Invariants
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={3}>
              <Typography variant="subtitle2" gutterBottom>
                Current Parameters
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                <Chip label={`p = ${params.p}`} color="primary" size="small" />
                <Chip label={`q = ${params.q}`} color="secondary" size="small" />
                <Chip label={`d = ${params.degree}`} size="small" />
                <Chip 
                  label={`mesh = ${params.meshDensity}×${params.meshDensity}`} 
                  size="small" 
                  variant="outlined"
                />
              </Box>
              <Typography variant="body2" sx={{ mt: 1, fontSize: '0.75rem', color: 'text.secondary' }}>
                Lattice: L<sub>d</sub> = ℤ(p·2<sup>-d</sup>) + ℤ(q·2<sup>-d</sup>·i)
              </Typography>
            </Grid>
            
            <Grid item xs={12} md={3}>
              <Typography variant="subtitle2" gutterBottom>
                Lattice Ratio (τ)
              </Typography>
              <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                {invariants.tau.real.toFixed(3)} + {invariants.tau.imag.toFixed(3)}i
              </Typography>
              <Typography variant="body2" sx={{ fontSize: '0.75rem', color: 'text.secondary' }}>
                τ = ω₂/ω₁
              </Typography>
            </Grid>
            
            <Grid item xs={12} md={3}>
              <Typography variant="subtitle2" gutterBottom>
                j-Invariant
              </Typography>
              {pythonInvariants?.usedPython ? (
                <Typography variant="body2" sx={{ fontFamily: 'monospace', color: 'success.main' }}>
                  {parseFloat(pythonInvariants.jInvariant).toExponential(3)}
                </Typography>
              ) : (
                <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                  {invariants.jInvariant.real.toFixed(1)} + {invariants.jInvariant.imag.toFixed(1)}i
                </Typography>
              )}
              <Typography variant="body2" sx={{ fontSize: '0.75rem', color: 'text.secondary' }}>
                j = 1728·g₂³/(g₂³-27g₃²)
              </Typography>
            </Grid>
            
            <Grid item xs={12} md={3}>
              <Typography variant="subtitle2" gutterBottom>
                Eisenstein Series
              </Typography>
              {pythonInvariants?.usedPython ? (
                <Box>
                  <Typography variant="body2" sx={{ fontFamily: 'monospace', fontSize: '0.8rem', color: 'success.main' }}>
                    g₂ ≈ {parseFloat(pythonInvariants.g2).toExponential(2)}
                  </Typography>
                  <Typography variant="body2" sx={{ fontFamily: 'monospace', fontSize: '0.8rem', color: 'success.main' }}>
                    g₃ ≈ {parseFloat(pythonInvariants.g3).toExponential(2)}
                  </Typography>
                  <Chip 
                    label="SymPy Computed" 
                    size="small" 
                    color="success" 
                    variant="outlined"
                    sx={{ mt: 0.5, fontSize: '0.7rem' }}
                  />
                </Box>
              ) : (
                <Box>
                  <Typography variant="body2" sx={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>
                    Δ = {invariants.discriminant.real.toFixed(1)} + {invariants.discriminant.imag.toFixed(1)}i
                  </Typography>
                  <Chip 
                    label="Classical" 
                    size="small" 
                    color="default" 
                    variant="outlined"
                    sx={{ mt: 0.5, fontSize: '0.7rem' }}
                  />
                </Box>
              )}
              <Typography variant="body2" sx={{ fontSize: '0.75rem', color: 'text.secondary' }}>
                g₂ = 60∑1/(mω₁+nω₂)⁴
              </Typography>
            </Grid>
          </Grid>
          
          {pythonInvariants?.usedPython && (
            <Box sx={{ mt: 2, p: 1, backgroundColor: 'success.main', color: 'success.contrastText', borderRadius: 1 }}>
              <Typography variant="body2" sx={{ fontSize: '0.85rem' }}>
                🐍 <strong>Python SymPy Backend Active:</strong> Using exact symbolic computation and elliptic function-based mesh generation with Weierstrass ℘ functions.
              </Typography>
            </Box>
          )}
          
          {!pythonInvariants?.usedPython && (
            <Box sx={{ mt: 2, p: 1, backgroundColor: 'warning.main', color: 'warning.contrastText', borderRadius: 1 }}>
              <Typography variant="body2" sx={{ fontSize: '0.85rem' }}>
                ⚡ <strong>Classical Mode:</strong> Using simplified parametric torus. Python backend loading or unavailable.
              </Typography>
            </Box>
          )}
        </AccordionDetails>
      </Accordion>
    </Paper>
  )
}

export default StatusBar