/*
  Team 84 - Melbourne
  Brendan Pichler(bpichler@student.unimelb.edu.au) 1212335
  George Wang (wagw@student.unimelb.edu.au) 1084224
  Luchen Zhou(luczhou@student.unimelb.edu.au) 1053412
  Wei Wang(wangw16@student.unimelb.edu.au) 900889
  Yihan Wang (yihwang3@student.unimelb.edu.au) 1056614
  */
import React, { useState } from 'react';
import politicalHtml from '../word_map/political.html';
import criminalHtml from '../word_map/criminal.html';
import employmentHtml from '../word_map/employment.html';
import trafficHtml from '../word_map/traffic.html';
import politicalImg from '../img/political_sudo.png';
import criminalImg from '../img/criminal_sudo.png';
import employmentImg from '../img/employment_sudo.png';
import trafficImg from '../img/traffic_sudo.png'
import { Container, Row, Col, Button, Dropdown, ButtonGroup } from 'react-bootstrap';

const TwitterData = () => {
  const [selectedHtml, setSelectedHtml] = useState(politicalHtml);
  const [topic, setTopic] = useState('Political');
  const [img, setImg] = useState(politicalImg);

  const handleDropdownChange = (selectedOption) => {
    setTopic(selectedOption);
    switch (selectedOption) {
      case 'political':
        setSelectedHtml(politicalHtml);
        setImg(politicalImg);
        break;
      case 'criminal':
        setSelectedHtml(criminalHtml);
        setImg(criminalImg);
        break;
      case 'employment':
        setSelectedHtml(employmentHtml);
        setImg(employmentImg)
        break;
      case 'traffic':
        setSelectedHtml(trafficHtml);
        setImg(trafficImg)
        break;
      default:
        setSelectedHtml('');
        setImg('')
    }
  };

  return (
    <Container>
      <Row>
        <Col sm={4}>
          <Dropdown onSelect={handleDropdownChange}>
            <Dropdown.Toggle variant="success" id="dropdown-basic" style={{ backgroundColor: '#4C70A2', borderColor: '#094183' }}>
              Select a topic
            </Dropdown.Toggle>
            <Dropdown.Menu>
              <Dropdown.Item eventKey="political">Political</Dropdown.Item>
              <Dropdown.Item eventKey="criminal">Criminal</Dropdown.Item>
              <Dropdown.Item eventKey="employment">Employment</Dropdown.Item>
              <Dropdown.Item eventKey="traffic">Traffic</Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </Col>
        <Col sm={8}>
          <h2>{topic.charAt(0).toUpperCase() + topic.slice(1)}</h2>
        </Col>
      </Row>
      <Row>
        <h3 style={{ 'paddingTop': '30px' }}>Twitter User and Post Data Analysis</h3>
        <div style={{ display: 'flex', justifyContent: 'center', margin: '20px 0' }}>
          {img && <img src={img} alt={topic} />}
        </div>
        <p>Ratio of twitter posts and twitter users in {topic.toLowerCase()} tweets.</p>
      </Row>
      <Row>
        <h3 style={{ 'paddingTop': '30px' }}>Twitter Region Map</h3>
        <p>Location of {topic.toLowerCase()} tweets made overlayed onto a map.</p>
        {selectedHtml && (
          <iframe
            title="HTML Content"
            srcDoc={selectedHtml}
            style={{ width: '100%', height: '800px', padding: '50px', paddingTop: '10px' }}
          />
        )}
      </Row>
    </Container>
  );
};

export default TwitterData;
