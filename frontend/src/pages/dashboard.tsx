import { useState } from 'react'
import { Link } from 'react-router-dom'
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline'
import "../styles/dashboard.css"

function Dashboard() {
    const [darkMode, setDarkMode] = useState(false)

    const toggleDarkMode = () => {
        setDarkMode((prev) => !prev)
    }

    return (
        <div id="dashboard" className={darkMode ? 'dark' : ''}>

            <section className="hero-dashboard">
                <h1>Mesh</h1>

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
            </section>

            <section className="sidebar">
                <Link className="active" to="/dashboard">
                    Home
                </Link>

                <Link to="/dashboard/tutorial">
                    Getting Started
                </Link>

                <Link to="/dashboard/documents">
                    Documents
                </Link>

                <Link to="/dashboard/changelog">
                    Changelog
                </Link>

                <Link to="/dashboard/about">
                    About
                </Link>
            </section>

        </div>
    )
}

export default Dashboard
