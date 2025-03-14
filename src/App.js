
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './component/Header';
import Home from './view/home';
import About from './view/about';
import Index from './view';

function App() {
    return (
        <main className="layout">
            <Router>
                <Header />
                <Routes>
                    <Route index element={<Home />} />
                    <Route path="about" element={<About />} />
                    <Route path="index" element={<Index />} />
                </Routes>
            </Router>
        </main>
    );
}

export default App;
