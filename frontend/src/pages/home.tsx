import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import "../styles/home.css"

interface HomeResponse {
  message: string
}

function Home() {
  const [message, setMessage] = useState<string>('Loading...')

  useEffect(() => {
    fetch('/home')
      .then((res) => res.json())
      .then((data: HomeResponse) => setMessage(data.message))
      .catch((err: unknown) => {
        console.error(err)
        setMessage('Failed to reach backend')
      })
  }, [])

return (
    <div className="home">
      <section className="hero">
        <h1 className="hero-title">Mesh</h1>
        <p className="hero-subtitle">
          Write, organize, and share documents — fast.
        </p>
        <div className="hero-actions">
          <Link to="/register" className="btn btn-primary">Get started</Link>
          <Link to="/login" className="btn btn-secondary">Log in</Link>
        </div>
        <p className="status-line">Backend status: <span>{message}</span></p>
      </section>
    </div>
  )
}

export default Home