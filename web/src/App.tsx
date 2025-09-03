import React, { useState } from 'react'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import { CssBaseline, Box } from '@mui/material'
import TorusVisualization from './components/TorusVisualization'
import ControlPanel from './components/ControlPanel'
import StatusBar from './components/StatusBar'

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    secondary: {
      main: '#f48fb1',
    },
    background: {
      default: '#1a1a1a',
      paper: '#2d2d2d',
    },
  },
})

export interface TorusParams {
  p: number
  q: number
  degree: number
  transparency: number
  meshDensity: number
  showWireframe: boolean
}

function App() {
  const [params, setParams] = useState<TorusParams>({
    p: 2,
    q: 3,
    degree: 1,
    transparency: 0.8,
    meshDensity: 20,
    showWireframe: true
  })

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ flex: 1, display: 'flex' }}>
          <Box sx={{ flex: 1 }}>
            <TorusVisualization params={params} />
          </Box>
          <Box sx={{ width: 300, borderLeft: '1px solid #444' }}>
            <ControlPanel params={params} setParams={setParams} />
          </Box>
        </Box>
        <StatusBar params={params} />
      </Box>
    </ThemeProvider>
  )
}

export default App