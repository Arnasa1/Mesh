import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline'
import "../styles/login.css"

interface LoginResponse {
  message: string
}

function Login() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  })

  const [showPassword, setShowPassword] = useState(false)
  const [message, setMessage] = useState<string>('')
  const [messageType, setMessageType] = useState<'success' | 'error' | ''>('')
  const [loading, setLoading] = useState(false)
  const [darkMode, setDarkMode] = useState(false)

  const navigate = useNavigate()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')
    setMessageType('')

    try {
      const res = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      const data: LoginResponse = await res.json()

      if (!res.ok) {
        throw new Error(data.message || 'Login failed')
      }

      setMessage(data.message || 'Logged in successfully!')
      setMessageType('success')

      setTimeout(() => {
        navigate('/dashboard')
      }, 1000)

    } catch (err) {
      setMessage(
        err instanceof Error ? err.message : 'Something went wrong'
      )
      setMessageType('error')
    } finally {
      setLoading(false)
    }
  }

  const toggleDarkMode = () => {
    setDarkMode((prev) => !prev)
  }

  return (
    <div className={`login ${darkMode ? 'dark' : ''}`}>
      <section className="hero-forms">

        <button
          type="button"
          className="theme-toggle"
          onClick={toggleDarkMode}
          aria-label="Toggle dark mode"
        >
          {darkMode ? (
            <SunIcon className="mode-icon" />
          ) : (
            <MoonIcon className="mode-icon" />
          )}
        </button>

        <h1 className="hero-title">Login</h1>

        <p className="hero-subtitle login-description">
          Log in to continue using Mesh.
        </p>

        <form onSubmit={handleSubmit}>
          <fieldset className="form-group">
            <label htmlFor="username">Username/Email</label>

            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </fieldset>

          <fieldset className="form-group">
            <label htmlFor="password">Password</label>

            <input
              type={showPassword ? 'text' : 'password'}
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />

            <label className="password-toggle">
              <input
                type="checkbox"
                checked={showPassword}
                onChange={(e) => setShowPassword(e.target.checked)}
              />
              Show password
            </label>
          </fieldset>

          {message && (
            <p className={`form-message ${messageType}`}>
              {message}
            </p>
          )}

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p className="hero-subtitle login-link">
          Don't have an account?{' '}
          <Link to="/register">Sign up</Link>
        </p>
      </section>
    </div>
  )
}

export default Login
