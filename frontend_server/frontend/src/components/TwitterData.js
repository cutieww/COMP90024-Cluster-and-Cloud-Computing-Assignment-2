import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Line, LineChart } from 'recharts';
import politicalHtml from '../word_map/political.html';
import criminalHtml from '../word_map/criminal.html';
import employmentHtml from '../word_map/employment.html';
import trafficHtml from '../word_map/traffic.html';

const TwitterData = () => {
  const [selectedHtml, setSelectedHtml] = useState('');
  const [topic, setTopic] = useState('');
  const [twitter, setTwitter] = useState({});
  const [sudo, setSudo] = useState({});

  const handleDropdownChange = (event) => {
    const selectedOption = event.target.value;
    setTopic(selectedOption);
    switch (selectedOption) {
      case 'political':
        setSelectedHtml(politicalHtml);
        break;
      case 'criminal':
        setSelectedHtml(criminalHtml);
        break;
      case 'employment':
        setSelectedHtml(employmentHtml);
        break;
      case 'traffic':
        setSelectedHtml(trafficHtml);
        break;
      default:
        setSelectedHtml('');
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://172.26.131.144/data/twitter_sudo/${topic}`);
        if (response.ok) {
          const data = await response.json();
          setTwitter(data.twitter);
          console.log(twitter)
          setSudo(data.sudo);
          console.log(sudo)
        } else {
          console.error(`Error fetching data: ${response.status}`);
        }
      } catch (error) {
        console.log('Error fetching data from the API:', error);
      }
    };
    fetchData();
  }, [topic]);

  const renderTwitterChart = () => {
    const chartData = Object.keys(twitter).map((key) => {
      const { user_ratio, tweet_ratio } = twitter[key];
      return { key, user_ratio, tweet_ratio };
    });
  
    return (
      <BarChart width={1200} height={400} data={chartData} >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="key" tick={{ fontSize: 15 }} interval={0} angle={45} textAnchor="start" />
        <YAxis yAxisId="left" />
        <YAxis yAxisId="right" orientation="right" />
        <Tooltip />
        <Legend verticalAlign="bottom" height={120} />
        <Bar dataKey="user_ratio" fill="#8884d8" name="User Ratio" yAxisId="left" />
        <Bar dataKey="tweet_ratio" fill="#82ca9d" name="Tweet Ratio" yAxisId="right" />
      </BarChart>
    );
  };

// ...

const renderSudoChart = () => {
  let chartData = [];
  let keyNames = [];

  switch (topic) {
    case 'criminal':
      chartData = Object.keys(sudo).map((dataKey) => {
        const data = sudo[dataKey];
        return { region: dataKey, ...data };
      });
      keyNames = Object.keys(sudo[Object.keys(sudo)[0]]);
      break;
    case 'employment':
      chartData = Object.keys(sudo).map((dataKey) => {
        const data = sudo[dataKey];
        return { state: dataKey, ...data };
      });
      keyNames = Object.keys(sudo[Object.keys(sudo)[0]]);
      break;
    case 'political':
      chartData = Object.keys(sudo).map((dataKey) => {
        const data = sudo[dataKey];
        return { state: dataKey, ...data };
      });
      keyNames = Object.keys(sudo[Object.keys(sudo)[0]]);
      break;
    case 'traffic':
      chartData = Object.keys(sudo).map((dataKey) => {
        const data = sudo[dataKey];
        return { state: dataKey, ...data };
      });
      keyNames = Object.keys(sudo[Object.keys(sudo)[0]]);
      break;
    default:
      chartData = [];
      keyNames = [];
  }

  const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff6e54', '#6b87c6', '#d096e2'];

  const threshold = 1;
  const dataLessThanThreshold = keyNames.filter((keyName) =>
    chartData.some((data) => data[keyName] < threshold)
  );

  return (
    <LineChart width={1200} height={400} data={chartData} margin={{ bottom: 50 }}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey={topic === 'criminal' ? 'region' : 'state'} tick={{ fontSize: 15 }} interval={0} angle={45} textAnchor="start" />
      <YAxis yAxisId="left" />
      <YAxis yAxisId="right" orientation="right" />
      <Tooltip />
      <Legend verticalAlign="bottom" height={120} />
      {keyNames.map((keyName, index) => {
        const yAxisId = dataLessThanThreshold.includes(keyName) ? 'right' : 'left';
        return (
          <Line
            key={index}
            type="monotone"
            dataKey={keyName}
            yAxisId={yAxisId}
            stroke={colors[index % colors.length]}
            name={keyName}
          />
        );
      })}
    </LineChart>
  );
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
      <div>
      <div>
        <h3>User Ratio and Tweet Ratio</h3>
        {Object.keys(twitter).length > 0 ? renderTwitterChart() : <p>Please Enter the topic.</p>}
        <h3>Sudo Data</h3>
        {Object.keys(sudo).length > 0 ? renderSudoChart() : <p>No Sudo Data Available.</p>}
    </div>
      </div>
      <h3>Words Map</h3>
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
