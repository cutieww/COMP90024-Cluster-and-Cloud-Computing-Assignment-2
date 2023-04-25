import React, { useState, useEffect } from 'react';
import { BarChart, XAxis, YAxis, Tooltip, CartesianGrid, Bar, Legend } from 'recharts';

const TwitterData = () => {
  const [data, setData] = useState([
    { name: 'Melbourne', value: 0 },
    { name: 'Sydney', value: 0 },
  ]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:8000/data');
      const text = await response.json();
      setData([
        { name: 'Melbourne', value: text.Melbourne },
        { name: 'Sydney', value: text.Sydney },
      ]);
    };

    const intervalId = setInterval(fetchData, 1000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div>
      <p>Melbourne: {data[0].value}</p>
      <p>Sydney: {data[1].value}</p>
      <BarChart
        width={500}
        height={300}
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="value" fill="#8884d8" />
      </BarChart>
    </div>
  );
};

export default TwitterData;
