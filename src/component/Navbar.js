import React from 'react';
import "./Header.css"
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
    
    const location = useLocation();

    return (
        <nav>
            <Link to="/" className={ location.pathname === "/" || location.pathname === "" ? "active nav" : 'nav' }>Home</Link>
            <Link to="/about" className={ location.pathname === "/about" ? "active nav" : 'nav' }>About</Link>
            <Link to="/index" className={ location.pathname === "/index" ? "active nav" : 'nav' }>Index</Link>
        </nav>
    );
};

export default Navbar;