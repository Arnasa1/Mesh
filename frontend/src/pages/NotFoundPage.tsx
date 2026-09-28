import { Link } from "react-router-dom"
import "../styles/main.css"
import "../styles/NotFoundPage.css"

const NotFoundPage = () => {
    return (
        <div className="NotFoundPage">
            <section>
            <h1>
                This page cannot be found 😡😡😡
            </h1>
            <Link to={"/"}>
                <button className="btn btn-primary nfp-btn">Go back Home</button>
            </Link>
            </section>
        </div>
    );
};

export default NotFoundPage;