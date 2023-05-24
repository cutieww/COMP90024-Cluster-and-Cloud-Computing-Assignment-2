/*
  Team 84 - Melbourne
  Brendan Pichler(bpichler@student.unimelb.edu.au) 1212335
  George Wang (wagw@student.unimelb.edu.au) 1084224
  Luchen Zhou(luczhou@student.unimelb.edu.au) 1053412
  Wei Wang(wangw16@student.unimelb.edu.au) 900889
  Yihan Wang (yihwang3@student.unimelb.edu.au) 1056614
  */
import './App.css';
import React, { useState } from 'react';
import { Route, Routes, Link, useLocation } from 'react-router-dom';
import HomePage from './components/HomePage';
import TwitterData from './components/TwitterData';
import MastodonData from './components/MastodonData';
import DataCompare from './components/DataCompare';
import AboutUs from './components/AboutUs';
import DataOverview from './components/DataOverview';
import { Nav, Container, Row, Col } from 'react-bootstrap';
import banner from './img/banner.jpg'

function App() {
  const location = useLocation();

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

  const getNavButtonClass = (nav) => currentLinkName !== nav ? 'nav-link-button' : 'nav-link-button-selected';

  const currentLinkName = getLinkName(location.pathname);

  return (
    <>
      <Container className='app-container' fluid>
        <Row>
          <Row
            className='banner'
            style={{
              'paddingBottom': '0px',
              'paddingRight': '0px',
              'backgroundImage': `url(${banner})`,
              'backgroundSize': 'cover',
              'backgroundPosition': 'center',
              'height': '15vh',
              'display': 'flex',
              'justifyContent': 'center',
              'alignItems': 'center'
            }}>

            <Col>
              <h1 className="text-center">Mastodon Twitter Analyser</h1>
            </Col>

          </Row>
          <Row style={{ 'paddingTop': '0px', 'paddingRight': '0px' }}>
            <Col sm={2} className='nav-bar'>
              <Nav defaultActiveKey="/" className="flex-column">
                <Nav.Link href="/" className={`${getNavButtonClass('Home')} nav-link-button`}>Home</Nav.Link>
                <Nav.Link href="/data-overview" className={`${getNavButtonClass('Data Overview')} nav-link-button`}>Data Overview</Nav.Link>
                <Nav.Link href="/twitter-data" className={`${getNavButtonClass('Twitter Data')} nav-link-button`}>Twitter Data</Nav.Link>
                <Nav.Link href="/mastodon-data" className={`${getNavButtonClass('Mastodon Data')} nav-link-button`}>Mastodon Data</Nav.Link>
                <Nav.Link href="/data-comparison" className={`${getNavButtonClass('Data Comparison')} nav-link-button`}>Data Comparison</Nav.Link>
                <Nav.Link href="/about-us" className={`${getNavButtonClass('About Us')} nav-link-button`}>About Us</Nav.Link>
              </Nav>
            </Col>

            <Col sm={10} className='main-content'>
              <Row className='subheading-ribbon'>
                <Col sm={10}>
                  <h2
                    className="text-center"
                    style={{
                      color: "#4C70A2",
                      fontSize: "2.5em"
                    }}>
                    {currentLinkName}
                  </h2>
                </Col>
              </Row>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/twitter-data" element={<TwitterData />} />
                <Route path='/data-overview' element={<DataOverview />} />
                <Route path="/mastodon-data" element={<MastodonData />} />
                <Route path='/data-comparison' element={<DataCompare />} />
                <Route path="/about-us" element={<AboutUs />} />
              </Routes>
            </Col>
          </Row>
        </Row>
      </Container>
      {/* </div> */}
      {/* </div> */}
    </>
  );
}

export default App;
