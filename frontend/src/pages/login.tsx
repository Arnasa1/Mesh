import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import "../styles/login.css"

interface LoginResponse {
  message: string
}

function Login() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  })
  const navigate = useNavigate();
  const [message, setMessage] = useState<string>('')
  const [messageType, setMessageType] = useState<'success' | 'error' | ''>('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    setMessageType('')

    try {
      const res = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
      const data: LoginResponse = await res.json()

      if (!res.ok) {
        setMessageType('error')
        throw new Error(data.message || 'Login failed')
      }

      setMessage(data.message || 'Logged in successfully!')
      setMessageType('success')
      setTimeout(() => {
        navigate("/dashboard")
      }, 1000);
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Something went wrong')
      setMessageType('error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login">
      <section className="hero">
        <h1 className="hero-title">Login</h1>

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
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </fieldset>

          {message && (<p className={`form-message ${messageType}`}>{message}</p>)}

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p className="hero-subtitle">
          Don't have an account? <Link to="/register">Sign up</Link>
        </p>
      </section>
    </div>
  )
}

export default Login