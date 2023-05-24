/*
  Team 84 - Melbourne
  Brendan Pichler(bpichler@student.unimelb.edu.au) 1212335
  George Wang (wagw@student.unimelb.edu.au) 1084224
  Luchen Zhou(luczhou@student.unimelb.edu.au) 1053412
  Wei Wang(wangw16@student.unimelb.edu.au) 900889
  Yihan Wang (yihwang3@student.unimelb.edu.au) 1056614
  */
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
