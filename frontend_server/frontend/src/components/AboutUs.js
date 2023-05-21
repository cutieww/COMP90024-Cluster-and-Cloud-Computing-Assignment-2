import React from 'react';

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
    <div>
      <div className="row">
        <div className="col-md-4">
          <Card name="Yihan Wang" role="Mastodon, CouchDB, Backend" />
        </div>
        <div className="col-md-4">
          <Card name="Wei Wang" role="Twitter, CouchDB, Backend" />
        </div>
        <div className="col-md-4">
          <Card name="George Wang" role="Ansible, Docker" />
        </div>
        <div className="col-md-4">
          <Card name="Brendan Pichler" role="React, Frontend" />
        </div>
        <div className="col-md-4">
          <Card name="Luchen Zhou" role="Infrastructure, Docker, Full stack" />
        </div>
      </div>
    </div>
  );
};

export default AboutUs;
