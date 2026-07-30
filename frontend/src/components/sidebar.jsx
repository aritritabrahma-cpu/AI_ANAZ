import "./Sidebar.css";
import { Link, useLocation } from "react-router-dom";

function Sidebar() {

    const location = useLocation();

    const menu = [

        {
            name: "Dashboard",
            path: "/"
        },

        {
            name: "Live APIs",
            path: "/live"
        },

        {
            name: "History",
            path: "/history"
        },

        {
            name: "Charts",
            path: "/charts"
        },

        {
            name: "Alerts",
            path: "/alerts"
        }

    ];

    return (

        <div className="sidebar">

            <div className="logo">

                Guardrail AI

            </div>

            {

                menu.map((item) => (

                    <Link
                        key={item.path}
                        to={item.path}
                        className={
                            location.pathname === item.path
                                ? "active"
                                : ""
                        }
                    >

                        {item.name}

                    </Link>

                ))

            }

        </div>

    );

}

export default Sidebar;