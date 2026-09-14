import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { toggleTheme } from '../scripts/themes'
import "../styles/home.css"
import "../styles/main.css"

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
      <script src="dist/theme.js" defer>
      </script>
      <section className="hero">
        <button
          id="theme-switch"
          onClick={toggleTheme}
          >
          <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#000000"><path d="M480-120q-150 0-255-105T120-480q0-150 105-255t255-105q14 0 27.5 1t26.5 3q-41 29-65.5 75.5T444-660q0 90 63 153t153 63q55 0 101-24.5t75-65.5q2 13 3 26.5t1 27.5q0 150-105 255T480-120Z"/></svg>
          <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#000000"><path d="M338.5-338.5Q280-397 280-480t58.5-141.5Q397-680 480-680t141.5 58.5Q680-563 680-480t-58.5 141.5Q563-280 480-280t-141.5-58.5ZM200-440H40v-80h160v80Zm720 0H760v-80h160v80ZM440-760v-160h80v160h-80Zm0 720v-160h80v160h-80ZM256-650l-101-97 57-59 96 100-52 56Zm492 496-97-101 53-55 101 97-57 59Zm-98-550 97-101 59 57-100 96-56-52ZM154-212l101-97 55 53-97 101-59-57Z"/></svg>
        </button>
        <h1 className="hero-title">Mesh</h1>
        <p className="hero-subtitle">
          Write, organize, and share documents — fast.
        </p>
        <div className="hero-actions">
          <Link to="/register" className="btn btn-primary">
            Get started
          </Link>
          <Link to="/login" className="btn btn-secondary">
            Log in
          </Link>
        </div>
        <p className="status-line">
          Backend status: <span>{message}</span>
        </p>
      </section>
    </div>
  )
}

export default Home
