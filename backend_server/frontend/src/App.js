import './App.css';
import React from 'react';
import { Route, Routes, Link } from 'react-router-dom';
import HomePage from './components/HomePage';
import TwitterData from './components/TwitterData';
import MastodonData from './components/MastodonData';
import AboutUs from './components/AboutUs';


function App() {
  return (
    <div>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/twitter-data">Twitter Data</Link>
          </li>
          <li>
            <Link to="/mastodon-data">Mastodon Data</Link>
          </li>
          <li>
            <Link to="/about-us">About Us</Link>
          </li>
        </ul>
      </nav>

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/twitter-data" element={<TwitterData />} />
        <Route path="/mastodon-data" element={<MastodonData />} />
        <Route path="/about-us" element={<AboutUs />} />
      </Routes>
    </div>
  );
}

export default App;
