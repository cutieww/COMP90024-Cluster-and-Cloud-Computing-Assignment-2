import React from 'react';
import SystemDesign from '../system_design.png'

const HomePage = () => {
  return (
    <div className="container">
      <div className="row">
        <h2>Application Overview</h2>
        <div id="overview" className="card">
            
        <p>Web application built on Melbourne Research Cloud to analyze Twitter data in Australia and world-wide Mastodon data in accordance to following topics:</p>
        <ul>
          <li>Political Topic</li>
          <li>Criminal Topic</li>
          <li>Employment Topic</li>
          <li>Traffic Topic</li>
        </ul>
        </div>
        <h2>System Design Graph</h2>
        <div className='design_graph'>
          <img alt='system design' src={SystemDesign} />
        </div>
      </div>
    </div>

  )
};

export default HomePage;