import { StrictMode, useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'

import Home from './pages/home'
import Register from './pages/register'
import Login from './pages/login'
import Dashboard from './pages/dashboard'
import DashboardItems from './scripts/DashboardItems'
import NotFoundPage from './pages/NotFoundPage'
import About from './pages/dashboardAbout'

import { initializeTheme } from './scripts/themes'

function Theme() {
  useEffect(() => {
    initializeTheme()
  }, [])

  return null
}

const router = createBrowserRouter([
  { path: '/', element: <Home /> },
  { path: '/register', element: <Register /> },
  { path: '/login', element: <Login /> },
  { path: '/dashboard', element: <Dashboard /> },
  { path: '/dashboard#About', element: <About /> },
  { path: '*', element: <NotFoundPage /> },
])

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Theme />
    <RouterProvider router={router} />
  </StrictMode>
)
