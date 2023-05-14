import React, { useState, useEffect } from 'react';
import { BarChart, XAxis, YAxis, Tooltip, CartesianGrid, Bar, Legend, PieChart, Pie, Cell } from 'recharts';
import ReactD3Cloud from 'react-d3-cloud';

const DataCompare = () => {
  const [date, setDate] = useState('');
  const [topic, setTopic] = useState('');
  const [mastodon, setMastodon] = useState({
    date: '',
    post_num: 0,
    total_post: 0,
    post_ratio: 0,
    user_ratio: 0,
    total_user: 0
  });


  const handleDateChange = async (event) => {
    const selectedDate = event.target.value;
    setDate(selectedDate);
  };

  const handleTopicChange = async (event) => {
    const selectedTopic = event.target.value;
    setTopic(selectedTopic);
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

  // Colors for the charts
  const COLORS = ['#0088FE', '#00C49F'];

  // Prepare word cloud data
  const wordCloudData = Object.entries(mastodon.wordmap || {})
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
    width: 200, // Set the width of the SVG canvas
    height: 100, // Set the height of the SVG canvas
  };


  return (
    <div className="container">
      <div className='row'>
      <div className="col-md-6">
        <h4>Graph for the mastodon data in {mastodon.date}</h4>

        <label htmlFor="date">Select a date:</label>
        <input type="date" id="date" name="date" value={date} onChange={handleDateChange} />

        <label htmlFor="topic">Select a topic:</label>
        <select id="topic" name="topic" value={topic} onChange={handleTopicChange}>
          <option value="">--Select a topic--</option>
          <option value="political">Political</option>
          <option value="criminal">Criminal</option>
          <option value="employment">Employment</option>
          <option value="traffic">Traffic</option>``
        </select>
        
      

        <h3>Mastodon Post Infromation - {topic}</h3>
        <div className='row'>
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
        <h4>Word Cloud</h4>
        <div style={{ width: '600px', height: '300px', overflow: 'scroll' }}>
          <ReactD3Cloud data={wordCloudData} {...wordCloudOptions} />
  
        </div>
        </div>
        </div>

        <div className="col-md-6">
          <h4>Graph for the Twitter data in </h4>
          {/* Add the additional content here */}
          
      </div>
      </div>
    </div>

  );
};

export default DataCompare;
