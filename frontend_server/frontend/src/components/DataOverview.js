import React, { useState, useEffect } from 'react';
import { BarChart, XAxis, YAxis, Tooltip, CartesianGrid, Bar, Legend, PieChart, Pie, Cell } from 'recharts';

const DataOverview = () => {
  const [mastodon, setMastodon] = useState({
    post_num: 0,
    total_post: 0,
    post_ratio: 0,
    user_num: 0,
    total_user: 0,
    user_ratio: 0,
  });

  const [twitter, setTwitter] = useState({
    post_num: 0,
    total_post: 0,
    post_ratio: 0,
    user_num: 0,
    total_user: 0,
    user_ratio: 0,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://172.26.131.144/data/twitter_data/all');
        if (response.ok) {
          const data = await response.json();
          console.log('Fetched data:', data);
          setTwitter(data);
        } else {
          console.error(`Error fetching data: ${response.status}`);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }

      try {
        const response = await fetch('http://172.26.131.144/data/mastodon_data/all');
        if (response.ok) {
          const data = await response.json();
          console.log('Fetched data:', data);
          setMastodon(data);
        } else {
          console.error(`Error fetching data: ${response.status}`);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      };

     
    };

    fetchData();
  }, []);

  return (
    <div className="container">
      <div className="row">
        <div className="col-md-6">
        <h3>Mastodon Post Information</h3>
        <p>Mastodon relevant post count: {mastodon.post_num}</p>
        <p>Total post count: {mastodon.total_post}</p>

        <BarChart
          width={500}
          height={300}
          data={[
            { name: 'relevant post', value: mastodon.post_num },
            { name: 'total Post', value: mastodon.total_post },
          ]}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
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
            data={[
              { name: 'relevant post', value: mastodon.post_ratio },
              { name: 'remaining ratio', value: 1 - mastodon.post_ratio },
            ]}
            cx={200}
            cy={100}
            labelLine={false}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            <Cell fill="#0088FE" />
            <Cell fill="#00C49F" />
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>

        <h4>User Ratio</h4>
        <PieChart width={400} height={200} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
          <Pie
            data={[
              { name: 'user with relevant post', value: mastodon.user_ratio },
              { name: 'remaining ratio', value: 1 - mastodon.user_ratio },
            ]}
            cx={200}
            cy={100}
            labelLine={false}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            <Cell fill="#0088FE" />
            <Cell fill="#00C49F" />
          </Pie>
          <Tooltip />
          <Legend/>
          </PieChart>
      </div>

      <div className="col-md-6">
         
        <h3>Twitter Post Information</h3>
        <p>Twitter relevant post count: {twitter.post_num}</p>
        <p>Total post count: {twitter.total_post}</p>

        <BarChart
          width={500}
          height={300}
          data={[
            { name: 'relevant post', value: twitter.post_num },
            { name: 'total Post', value: twitter.total_post },
          ]}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
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
            data={[
              { name: 'relevant post', value: twitter.post_ratio },
              { name: 'remaining ratio', value: 1 - twitter.post_ratio },
            ]}
            cx={200}
            cy={100}
            labelLine={false}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            <Cell fill="#0088FE" />
            <Cell fill="#00C49F" />
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>

        <h4>User Ratio</h4>
        <PieChart width={400} height={200} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
          <Pie
            data={[
              { name: 'user with relevant post', value: twitter.user_ratio },
              { name: 'remaining ratio', value: 1 - twitter.user_ratio },
            ]}
            cx={200}
            cy={100}
            labelLine={false}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            <Cell fill="#0088FE" />
            <Cell fill="#00C49F" />
          </Pie>
          <Tooltip />
          <Legend/>
          </PieChart>
        
      </div>
    </div>
 </div>

  );
};

export default DataOverview;

