import React, { useState, useEffect } from 'react';
import { BarChart, XAxis, YAxis, Tooltip, CartesianGrid, Bar, Legend, PieChart, Pie, Cell } from 'recharts';
import ReactD3Cloud from 'react-d3-cloud';
import { Container, Row, Col, Table, Button, Dropdown, ButtonGroup } from 'react-bootstrap';


const DataCompare = () => {
  const [date, setDate] = useState('2023-05-21');
  const [topic, setTopic] = useState('political');
  const [mastodon, setMastodon] = useState({
    date: '',
    post_num: 0,
    total_post: 0,
    post_ratio: 0,
    user_ratio: 0,
    total_user: 0
  });

  const [selectedState, setSelectedState] = useState('Queensland');
  const [twitterTopic, setTwitterTopic] = useState('political');
  const [twitter, setTwitter] = useState({
    date: '',
    tweet_count: 0,
    total_tweet_count: 0,
    tweet_ratio: 0,
    user_ratio: 0,
    total_user_count: 0,
    word_cloud: {}
  });


  const handleDateChange = async (event) => {
    const selectedDate = event.target.value;
    setDate(selectedDate);
  };

  const handleTopicChange = async (selectedTopic) => {
    setTopic(selectedTopic);
  };

  const handleStateChange = async (selectedState) => {
    setSelectedState(selectedState);
  };

  const handleTwitterTopicChange = async (selectedTopic) => {
    setTwitterTopic(selectedTopic);
  };


  useEffect(() => {
    const fetchData = async () => {
      if (date) {
        const response = await fetch(`http://172.26.131.144/data/mastodon_data/query/${topic}/${date}`);
        if (response.ok) {
          const data = await response.json();
          console.log('Fetched data:', data); // Add this line
          setMastodon(data);
        } else {
          console.error(`Error fetching data: ${response.status}`);
        }
      }
    };

    fetchData();
  }, [date, topic]);

  useEffect(() => {
    const fetchData = async () => {
      if (selectedState) {
        const response = await fetch(`http://172.26.131.144/data/twitter_data/query/${twitterTopic}/${selectedState}`);
        if (response.ok) {
          const data = await response.json();
          console.log('Fetched Twitter data:', data);
          setTwitter(data);
        } else {
          console.error(`Error fetching Twitter data: ${response.status}`);
        }
      }
    };

    fetchData();
  }, [twitterTopic, selectedState]);


  // Bar chart data
  const barChartData = [
    { name: topic + ' post', value: mastodon.post_num },
    { name: 'total post', value: mastodon.total_post },
  ];

  // Pie chart data
  const postRatioData = [
    { name: topic + ' post', value: mastodon.post_ratio },
    { name: 'remaining ratio', value: 1 - mastodon.post_ratio },
  ];

  const userRatioData = [
    { name: topic + ' post', value: mastodon.user_ratio },
    { name: 'remaining ratio', value: 1 - mastodon.user_ratio },
  ];

  // Twitter Bar chart data
  const twitterBarChartData = [
    { name: topic + ' tweet', value: twitter.tweet_count },
    { name: 'total tweet', value: twitter.total_tweet_count },
  ];

  // Twitter Pie chart data
  const twitterTweetRatioData = [
    { name: topic + ' tweet', value: twitter.tweet_ratio },
    { name: 'remaining ratio', value: 1 - twitter.tweet_ratio },
  ];

  const twitterUserRatioData = [
    { name: topic + ' tweet', value: twitter.user_ratio },
    { name: 'remaining ratio', value: 1 - twitter.user_ratio },
  ];


  // Colors for the charts
  const COLORS = ['#0088FE', '#00C49F'];

  const minMaxNormalize = (data, minSize, maxSize) => {
    if (data.length === 0) {
      return data;
    }

    const max = Math.max(...data.map(item => item.value));
    const min = Math.min(...data.map(item => item.value));

    return data.map(item => ({
      ...item,
      value: ((item.value - min) / (max - min)) * (maxSize - minSize) + minSize
    }));
  }


  // Prepare word cloud data
  // Prepare word cloud data
  const wordCloudData = minMaxNormalize(
    Object.entries(mastodon.wordmap || {})
      .map(([text, value]) => ({ text, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 200),
    1000, // min size
    10000 // max size
  );


  const twitterWordCloudData = Object.entries(twitter.word_cloud || {})
    .map(([text, value]) => ({ text, value }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 200);

  /*
  const userCloudData = Object.entries(mastodon.usermap || {})
    .map(([text, value]) => ({ text, value }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 50);
  */

  // Define word cloud options
  const wordCloudOptions = {
    rotations: 2,
    rotationAngles: [0, 90], // Words will be either horizontal (0 degrees) or vertical (90 degrees)
    fontSizes: [80, 120], // Increase the minimum font size
    fontWeight: 'bold',
    padding: -2, // Decrease the padding between words
    width: 1000, // Set the width of the SVG canvas
    height: 500, // Set the height of the SVG canvas
  };


  return (
    <Container>
      <Row>
        <Col>
          <Row style={{ 'padding': '10px' }}>
            <h4>Graph for the mastodon data in {mastodon.date}</h4>
            <div>
              <label htmlFor="date">Select a date: </label>
              <input type="date" id="date" name="date" value={date} onChange={handleDateChange} />
            </div>
          </Row>
          <Row style={{ 'padding': '10px' }}>
            <Col sm={4}>
              Select a topic:
            </Col>
            <Col sm={8}>
              <Dropdown onSelect={handleTopicChange}>
                <Dropdown.Toggle variant="success" id="dropdown-basic">
                  {topic.charAt(0).toUpperCase() + topic.slice(1)}
                </Dropdown.Toggle>
                <Dropdown.Menu>
                  <Dropdown.Item eventKey="political">Political</Dropdown.Item>
                  <Dropdown.Item eventKey="criminal">Criminal</Dropdown.Item>
                  <Dropdown.Item eventKey="employment">Employment</Dropdown.Item>
                  <Dropdown.Item eventKey="traffic">Traffic</Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </Col>
          </Row>
          <h3 style={{ 'paddingTop': '20px' }}>Mastodon Post Infromation - {topic.charAt(0).toUpperCase() + topic.slice(1)}</h3>
          <Row>
            <div style={{ 'padding': '10px' }}>
              <p>{topic} post count: {mastodon.post_num}</p>
              <p>Total post count: {mastodon.total_post} </p>
              <BarChart
                width={500}
                height={300}
                data={barChartData}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8" />
              </BarChart>
            </div>
            <div style={{ 'padding': '10px' }}>
              <h4>Post Ratio</h4>
              <PieChart width={400} height={200} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                <Pie
                  data={postRatioData}
                  cx={200}
                  cy={100}
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {postRatioData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </div>
            <div style={{ 'padding': '10px' }}>
              <h4>User Ratio</h4>
              <PieChart width={400} height={200} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                <Pie
                  data={userRatioData}
                  cx={200}
                  cy={100}
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {userRatioData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </div>
            {/*
        <h4>Top 10 Users</h4>
        <ol>
          {userCloudData.slice(0, 10).map((user, index) => (
            <li key={index}>
              {user.text} (Posts: {user.value})
            </li>
          ))}
        </ol>
          */}
            <div style={{ 'padding': '10px' }}>
              <h4>Mastodon Word Cloud</h4>
              <div style={{ width: '600px', height: '300px', overflow: 'scroll' }}>
                <ReactD3Cloud data={wordCloudData} {...wordCloudOptions} />
              </div>
            </div>
          </Row>
        </Col>
        <Col>
          <Row>
            <h4>Graph for the Twitter data in {twitter.date}</h4>
          </Row>
          <Row style={{ 'padding': '10px' }}>
            <Col sm={4}>
              Select a state:
            </Col>
            <Col sm={8}>
              <Dropdown onSelect={handleStateChange}>
                <Dropdown.Toggle variant="success" id="dropdown-basic">
                  {selectedState.replaceAll('_', ' ')}
                </Dropdown.Toggle>
                <Dropdown.Menu>
                  <Dropdown.Item eventKey="Queensland">Queensland</Dropdown.Item>
                  <Dropdown.Item eventKey="Western_Australia">Western Australia</Dropdown.Item>
                  <Dropdown.Item eventKey="New_South_Wales">New South Wales</Dropdown.Item>
                  <Dropdown.Item eventKey="Victoria">Victoria</Dropdown.Item>
                  <Dropdown.Item eventKey="Northern_Territory">Northern Territory</Dropdown.Item>
                  <Dropdown.Item eventKey="South_Australia">South Australia</Dropdown.Item>
                  <Dropdown.Item eventKey="Tasmania">Tasmania</Dropdown.Item>
                  <Dropdown.Item eventKey="Australian_Capital_Territory">Australian Capital Territory</Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </Col>
          </Row>
          <Row style={{ 'padding': '10px' }}>
            <Col sm={4}>
              Select a topic:
            </Col>
            <Col sm={8}>
              <Dropdown onSelect={handleTwitterTopicChange}>
                <Dropdown.Toggle variant="success" id="dropdown-basic">
                  {twitterTopic.charAt(0).toUpperCase() + twitterTopic.slice(1)}
                </Dropdown.Toggle>
                <Dropdown.Menu>
                  <Dropdown.Item eventKey="political">Political</Dropdown.Item>
                  <Dropdown.Item eventKey="criminal">Criminal</Dropdown.Item>
                  <Dropdown.Item eventKey="employment">Employment</Dropdown.Item>
                  <Dropdown.Item eventKey="traffic">Traffic</Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </Col>
          </Row>

          <h3 style={{ 'paddingTop': '20px' }}>Twitter Tweet Information - {twitterTopic.charAt(0).toUpperCase() + twitterTopic.slice(1)}</h3>
          <Row>
            <div style={{ 'padding': '10px' }}>
              <p>{topic} tweet count: {twitter.tweet_count}</p>
              <p>Total tweet count: {twitter.total_tweet_count} </p>
              <BarChart
                width={500}
                height={300}
                data={twitterBarChartData}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8" />
              </BarChart>
            </div>

            <div style={{ 'padding': '10px' }}>
              <h4>Tweet Ratio</h4>
              <PieChart width={400} height={200} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                <Pie
                  data={twitterTweetRatioData}
                  cx={200}
                  cy={100}
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {twitterTweetRatioData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </div>

            <div style={{ 'padding': '10px' }}>
              <h4>User Ratio</h4>
              <PieChart width={400} height={200} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                <Pie
                  data={twitterUserRatioData}
                  cx={200}
                  cy={100}
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {twitterUserRatioData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </div>

            <div style={{ 'padding': '10px' }}>
              <h4>Twitter Word Cloud</h4>
              <div style={{ width: '600px', height: '300px', overflow: 'scroll' }}>
                <ReactD3Cloud data={twitterWordCloudData} {...wordCloudOptions} />
              </div>
            </div>
          </Row>
        </Col>

      </Row>
    </Container>

  );
};

export default DataCompare;
