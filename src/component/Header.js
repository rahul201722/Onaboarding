import React from "react";
import "./Header.css"
import Navbar from './Navbar'

const Header = () => {
    return (
        <header className="just-between align-center header">
            <div>
                <p className="title f_bold">UV Protect</p>
                <p className="desc">Uv index tips and skin protection</p>
            </div>
            <Navbar />
        </header>
    )
}

export default Header