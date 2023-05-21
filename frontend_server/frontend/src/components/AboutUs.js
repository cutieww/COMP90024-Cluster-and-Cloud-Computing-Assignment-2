import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const Card = ({ name, role }) => {
  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title">{name}</h5>
        <p className="card-text">In charge of: </p>
        <p>{role}</p>
      </div>
    </div>
  );
};

const AboutUs = () => {
  return (
    <Container>
      <Row>
        <Col sm={4}>
          <Card name="Yihan Wang" role="Mastodon, CouchDB, Backend" />
        </Col>
        <Col sm={4}>
          <Card name="Wei Wang" role="Twitter, CouchDB, Backend" />
          </Col>
        <Col sm={4}>
          <Card name="George Wang" role="Ansible, Docker" />
          </Col>
        <Col sm={4}>
          <Card name="Brendan Pichler" role="React, Frontend" />
        </Col>
        <Col sm={4}>
          <Card name="Luchen Zhou" role="Infrastructure, Docker, Full stack" />
        </Col>
      </Row>
    </Container>
  );
};

export default AboutUs;
