import React, { useState, useEffect } from 'react';
import { BarChart, XAxis, YAxis, Tooltip, CartesianGrid, Bar, Legend } from 'recharts';

const MastodonData = () => {
  const [data, setData] = useState(
    { name: 'Count', value: 0 }
  );

  useEffect(() => {
    const fetchData = async () => {
      //const response = await fetch('http://localhost:8000/mastodon_data');
      const response = await fetch('http://172.26.132.54:8000/mastodon_data');
      const text = await response.json();
      setData(
        { name: 'Count', value: text.number },
      );
    };

    const intervalId = setInterval(fetchData, 1000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div>
      <p>Count: {data.value}</p>
      <BarChart
        width={500}
        height={300}
        data={[{ name: 'Count', value: data.value }]}
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

export default MastodonData;