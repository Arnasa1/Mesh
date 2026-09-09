import { Link } from 'react-router-dom'
import '../styles/dashboard.css'

function Dashboard() {
    return (
        <div id="dashboard">
            <section className="hero-dashboard">
                <h1>Mesh</h1>
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
