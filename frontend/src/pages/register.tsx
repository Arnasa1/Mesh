import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { toggleTheme } from '../scripts/themes'
import "../styles/register.css"
import "../styles/main.css"

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

  return (
    <div className="register">
      <section className="hero-forms">
        <button
          id="theme-switch"
          onClick={toggleTheme}
          >
          <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#000000"><path d="M480-120q-150 0-255-105T120-480q0-150 105-255t255-105q14 0 27.5 1t26.5 3q-41 29-65.5 75.5T444-660q0 90 63 153t153 63q55 0 101-24.5t75-65.5q2 13 3 26.5t1 27.5q0 150-105 255T480-120Z"/></svg>
          <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#000000"><path d="M338.5-338.5Q280-397 280-480t58.5-141.5Q397-680 480-680t141.5 58.5Q680-563 680-480t-58.5 141.5Q563-280 480-280t-141.5-58.5ZM200-440H40v-80h160v80Zm720 0H760v-80h160v80ZM440-760v-160h80v160h-80Zm0 720v-160h80v160h-80ZM256-650l-101-97 57-59 96 100-52 56Zm492 496-97-101 53-55 101 97-57 59Zm-98-550 97-101 59 57-100 96-56-52ZM154-212l101-97 55 53-97 101-59-57Z"/></svg>
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