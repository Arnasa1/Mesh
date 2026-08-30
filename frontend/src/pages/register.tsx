import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
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
      const res = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
      const data: RegisterResponse = await res.json()

      if (!res.ok) {
        setMessageType('error')
        throw new Error(data.message || 'Registration failed')
      }

      setMessage(data.message || 'Registered successfully!')
      setMessageType('success')
      setTimeout(() => {
        navigate("/login")
      }, 1000);

    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Something went wrong')
      setMessageType('error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="register">
      <section className="hero">
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
            {loading ? 'Registering...' : 'Register'}
          </button>
        </form>

        <p className="hero-subtitle">
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </section>
    </div>
  )
}

export default Register