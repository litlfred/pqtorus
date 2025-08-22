import React from 'react'
import { Paper, Typography, Grid, Box, Chip } from '@mui/material'
import { TorusParams } from '../App'
import { calculateEllipticInvariants } from '../utils/ellipticMath'

interface StatusBarProps {
  params: TorusParams
}

function StatusBar({ params }: StatusBarProps) {
  const invariants = calculateEllipticInvariants(params.p, params.q)
  
  return (
    <Paper sx={{ p: 2, borderRadius: 0 }}>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} md={3}>
          <Typography variant="h6" gutterBottom>
            Current Parameters
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <Chip label={`p = ${params.p}`} color="primary" size="small" />
            <Chip label={`q = ${params.q}`} color="secondary" size="small" />
            <Chip label={`d = ${params.degree}`} size="small" />
          </Box>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Typography variant="subtitle2" gutterBottom>
            Lattice Ratio (τ)
          </Typography>
          <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
            {invariants.tau.real.toFixed(3)} + {invariants.tau.imag.toFixed(3)}i
          </Typography>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Typography variant="subtitle2" gutterBottom>
            j-Invariant
          </Typography>
          <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
            {invariants.jInvariant.real.toFixed(1)} + {invariants.jInvariant.imag.toFixed(1)}i
          </Typography>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Typography variant="subtitle2" gutterBottom>
            Discriminant
          </Typography>
          <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
            {invariants.discriminant.real.toFixed(1)} + {invariants.discriminant.imag.toFixed(1)}i
          </Typography>
        </Grid>
      </Grid>
    </Paper>
  )
}

export default StatusBar