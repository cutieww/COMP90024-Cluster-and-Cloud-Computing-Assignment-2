/*
  Team 84 - Melbourne
  Brendan Pichler(bpichler@student.unimelb.edu.au) 1212335
  George Wang (wagw@student.unimelb.edu.au) 1084224
  Luchen Zhou(luczhou@student.unimelb.edu.au) 1053412
  Wei Wang(wangw16@student.unimelb.edu.au) 900889
  Yihan Wang (yihwang3@student.unimelb.edu.au) 1056614
  */
import React from 'react';
import SystemDesign from '../system_design.png'
import { Container, Row, Col, Button } from 'react-bootstrap';

const HomePage = () => {
  return (
    <Container>
      <Row>
        <Col>
        <Row>
        <h2>Application Overview</h2>
        </Row>
        <div id="overview">
            
        <p>Web application built on Melbourne Research Cloud to analyze Twitter data in Australia and world-wide Mastodon data in accordance to following topics:</p>
        <ul>
          <li>Political Topic</li>
          <li>Criminal Topic</li>
          <li>Employment Topic</li>
          <li>Traffic Topic</li>
        </ul>
        </div>
        <Row>
        <h2>System Design Graph</h2>
        <div className='design_graph'>
          <img alt='system design' src={SystemDesign} />
        </div>
        </Row>
        </Col>
      </Row>
    </Container>

  )
};

export default HomePage;