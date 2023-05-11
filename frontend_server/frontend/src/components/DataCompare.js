import React, { useState, useEffect } from 'react';
import { BarChart, XAxis, YAxis, Tooltip, CartesianGrid, Bar, Legend, PieChart, Pie, Cell } from 'recharts';

const DataCompare = () => {
  const [date, setDate] = useState('');
  const [mastodon, setMastodon] = useState({
    date: '',
    count: 0,
    total_post: 0,
    post_ratio: 0,
    user_ratio: 0,
    user_total: 0,
  });


  const handleDateChange = async (event) => {
    const selectedDate = event.target.value;
    setDate(selectedDate);
  };

  useEffect(() => {
    const fetchData = async () => {
      if (date) {
        const response = await fetch(`http://172.26.131.144/data/mastodon_data/date/${date}`);
        if (response.ok) {
          const data = await response.json();
          setMastodon(data);
        } else {
          console.error(`Error fetching data: ${response.status}`);
        }
      }
    };

    fetchData();
  }, [date]);

  // Bar chart data
    const barChartData = [
    { name: 'Political Post', value: mastodon.count },
    { name: 'Total Post', value: mastodon.total_post },
  ];

  // Pie chart data
  const postRatioData = [
    { name: 'political post', value: mastodon.post_ratio },
    { name: 'remaining ratio', value: 1 - mastodon.post_ratio },
  ];

  const userRatioData = [
    { name: 'user with political post', value: mastodon.user_ratio },
    { name: 'remaining ratio', value: 1 - mastodon.user_ratio },
  ];

  // Colors for the charts
  const COLORS = ['#0088FE', '#00C49F'];

  return (
    <div>
        <h1>Data Compare</h1>
        <h4>Graph for the mastodon data in {mastodon.date}</h4>
        <label htmlFor="date">Select a date:</label>
        <input type="date" id="date" name="date" value={date} onChange={handleDateChange} />
        <BarChart
        width={500}
        height={300}
        data={barChartData}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
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
    </div>
  );
};

export default DataCompare;
