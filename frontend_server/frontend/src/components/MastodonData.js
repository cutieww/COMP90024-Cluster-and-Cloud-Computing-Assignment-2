import React, { useState, useEffect } from 'react';
import { BarChart, XAxis, YAxis, Tooltip, CartesianGrid, Bar, Legend, PieChart, Pie, Cell} from 'recharts';


const MastodonData = () => {
  const [data, setData] = useState(
    { host: "", date: "", count: 0, total_post: 0, post_ratio: 0, user_ratio: 0}
  );
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleString()); // initialize the current time state

  const [post, setPost] = useState(
    { username: "", token: "", created_at:"", political_related:""}
  )

  const [userMap, setUserMap] = useState({});
  const [wordMap, setWordMap] = useState({});

  const [countdown, setCountdown] = useState(5);

  useEffect(() => {
    const fetchData = async () => {
      // Fetch mastodon_data API
      //const response = await fetch('http://172.26.129.100:8000/mastodon_data');
      //const response = await fetch('http://localhost:80/mastodon_data'); // fetch from the nginx proxy, which listens on port 80
      const response = await fetch('http://172.26.131.144/data/mastodon_data');

      if (response.ok) { // Check if the response status is OK (200)
      const text = await response.json();

      setData({
        host: text.host,
        date: text.date,
        count: text.count,
        total_post: text.total_post,
        post_ratio: text.post_ratio,
        user_ratio: text.user_ratio,
      });

      setPost({
        username: text.latest_post.username,
        token: text.latest_post.token,
        created_at: text.latest_post.created_at,
        political_related: text.latest_post.political_related ? 'Yes' : 'No',
      });
    } else {
      console.error(`Error fetching data: ${response.status}`);
    }

    // Fetch mastodon_map API
    const mapResponse = await fetch('http://172.26.131.144/data/mastodon_map');

    if (mapResponse.ok) {
      const json = await mapResponse.json();
      setUserMap(json.usermap);
      setWordMap(json.wordmap);
    } else {
      console.error(`Error fetching map data: ${mapResponse.status}`);
    }

        setCurrentTime(new Date().toLocaleString()); // update the current time state

    };


    const updateTime = () => {

      setCountdown((prevCountdown) => (prevCountdown > 1 ? prevCountdown - 1 : 5));
    };

    const fetchDataIntervalId = setInterval(fetchData, 5000);
    const updateTimeIntervalId = setInterval(updateTime, 1000);

    return () => {
      clearInterval(fetchDataIntervalId);
      clearInterval(updateTimeIntervalId);
    };
  }, []);

  const COLORS = ['#0088FE', '#00C49F'];
  const barChartData = [
    { name: 'Political Post', value: data.count },
    { name: 'Total Post', value: data.total_post },
  ];

  const postRatioData = [
    { name: 'political post', value: data.post_ratio },
    { name: 'remaining ratio', value: 1 - data.post_ratio },
  ];

  const userRatioData = [
    { name: 'user with political post', value: data.user_ratio },
    { name: 'remaining ratio', value: 1 - data.user_ratio },
  ];
  return (
    <div>
      <p>Next update in {countdown} seconds</p>
      <p>Data was retrieved from host {data.host} successfully at {currentTime}</p>

      <h4>Latest post streamed</h4>
      <p>Username: {post.username}</p>
      <p>Tokens: {post.token}</p>
      <p>Created_at: {post.created_at}</p>
      <p>political_related: {post.political_related}</p>

      <h4>Data Summary in {data.date}</h4>
      <p>Count: {data.count}</p>
      <p>Total Count: {data.total_post}</p>

      <BarChart
        width={500}
        height={300}
        data={barChartData}
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

      <h4>User Map</h4>
      <ul>
        {Object.entries(userMap).map(([key, value]) => (
          <li key={key}>
            {key}: {value}
          </li>
        ))}
      </ul>

      <h4>Word Map</h4>
      <ul>
        {Object.entries(wordMap).map(([key, value]) => (
          <li key={key}>
            {key}: {value}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MastodonData;
