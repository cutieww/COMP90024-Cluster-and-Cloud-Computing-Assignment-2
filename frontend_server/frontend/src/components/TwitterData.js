import React, { useState} from 'react';
import politicalHtml from '../word_map/political.html';
import criminalHtml from '../word_map/criminal.html';
import employmentHtml from '../word_map/employment.html';
import trafficHtml from '../word_map/traffic.html';
import politicalImg from '../img/political_sudo.png';
import criminalImg from '../img/criminal_sudo.png';
import employmentImg from '../img/employment_sudo.png';
import trafficImg from '../img/traffic_sudo.png'

const TwitterData = () => {
  const [selectedHtml, setSelectedHtml] = useState(politicalHtml);
  const [topic, setTopic] = useState('political');
  const [img, setImg] = useState(politicalImg);

  const handleDropdownChange = (event) => {
    const selectedOption = event.target.value;
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
    <div>
      <select onChange={handleDropdownChange}>
        <option value="">--Select a topic--</option>
        <option value="political">Political</option>
        <option value="criminal">Criminal</option>
        <option value="employment">Employment</option>
        <option value="traffic">Traffic</option>
      </select>
      <div style={{ display: 'flex', justifyContent: 'center', margin: '20px 0' }}>
        {img && <img src={img} alt={topic} />}
      </div>
      <h3>Twitter Region Map</h3>
      {selectedHtml && (
        <iframe
          title="HTML Content"
          srcDoc={selectedHtml}
          style={{ width: '100%', height: '800px' }}
        />
      )}
    </div>
  );
};

export default TwitterData;
