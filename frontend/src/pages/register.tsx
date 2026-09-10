import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline'
import "../styles/register.css"

interface RegisterResponse {
  message: string
}

function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
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
      const res = await fetch('/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      const data: RegisterResponse = await res.json()

      if (!res.ok) {
        throw new Error(data.message || 'Registration failed')
      }

      setMessage(data.message || 'Registered successfully!')
      setMessageType('success')

      setTimeout(() => {navigate('/login')}, 1000)} catch (err) {
      setMessage(
        err instanceof Error ? err.message : 'Something went wrong')
      setMessageType('error')
    } finally {
      setLoading(false)
    }
  }

  const toggleDarkMode = () => {
    setDarkMode((prev) => !prev)
  }

  return (
    <div className={`register ${darkMode ? 'dark' : ''}`}>
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

        <h1 className="hero-title">Register</h1>

        <p className="hero-subtitle">
          Create an account to start using Mesh.
        </p>

        <form onSubmit={handleSubmit}>
          <fieldset className="form-group">
            <label htmlFor="username">Username</label>

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
            <label htmlFor="email">Email</label>

            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
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
            {loading ? 'Registering...' : 'Register'}
          </button>
        </form>

        <p className="hero-subtitle login-link">
          Already have an account?{' '}
          <Link to="/login">Log in</Link>
        </p>
      </section>
    </div>
  )
}

export default Register