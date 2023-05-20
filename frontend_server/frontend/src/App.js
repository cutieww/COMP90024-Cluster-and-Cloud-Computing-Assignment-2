import './App.css';
import React, { useState } from 'react';
import { Route, Routes, Link, useLocation } from 'react-router-dom';
import HomePage from './components/HomePage';
import TwitterData from './components/TwitterData';
import MastodonData from './components/MastodonData';
import DataCompare from './components/DataCompare';
import AboutUs from './components/AboutUs';
import DataOverview from './components/DataOverview';
import { BsChevronDoubleLeft, BsChevronDoubleRight } from 'react-icons/bs';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const location = useLocation();

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const getLinkName = (path) => {
    switch (path) {
      case '/':
        return 'Home';
      case '/data-overview':
        return 'Data Overview';
      case '/twitter-data':
        return 'Twitter Data';
      case '/mastodon-data':
        return 'Mastodon Data';
      case '/data-comparison':
        return 'Data Comparison';
      case '/about-us':
        return 'About Us';
      default:
        return '';
    }
  };

  const currentLinkName = getLinkName(location.pathname);

  return (
    <div className="container-fluid">
      <div className="row">
        <div id="Sidebar-button" className="col-sm-0.1 d-flex align-items-center">
          <button
            type="button"
            className={`btn btn-primary sidebar-toggle-btn ${sidebarOpen ? 'open' : 'closed'}`}
            onClick={toggleSidebar}
          >
            {sidebarOpen ? <BsChevronDoubleLeft /> : <BsChevronDoubleRight />}
          </button>
          <div className={`sidebar-title ${sidebarOpen ? '' : 'show'}`}>
            <h1>{currentLinkName}</h1>
          </div>
        </div>
        <div className={`col-md-2 sidebar bg-light ${sidebarOpen ? '' : 'd-none'}`}>
          <nav className={`nav flex-column d-md-block`}>
            <Link className="nav-link" to="/">Home</Link>
            <Link className="nav-link" to="/data-overview">Data Overview</Link>
            <Link className="nav-link" to="/twitter-data">Twitter Data</Link>
            <Link className="nav-link" to="/mastodon-data">Mastodon Streaming</Link>
            <Link className="nav-link" to="/data-comparison">Data Comparison</Link>
            <Link className="nav-link" to="/about-us">About Us</Link>
          </nav>
        </div>
        <div className="col-md-10">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/twitter-data" element={<TwitterData />} />
            <Route path='/data-overview' element={<DataOverview/>}/>
            <Route path="/mastodon-data" element={<MastodonData />} />
            <Route path='/data-comparison' element={<DataCompare/>}/>
            <Route path="/about-us" element={<AboutUs />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default App;
