import React, { useState, useEffect } from 'react';
import { BarChart, XAxis, YAxis, Tooltip, CartesianGrid, Bar, Legend, PieChart, Pie, Cell} from 'recharts';
import DOMPurify from 'dompurify';


const MastodonData = () => {
  const [data, setData] = useState(
    { host: "", date: "", count: 0, total_post: 0, post_ratio: 0, user_ratio: 0}
  );
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleString()); // initialize the current time state

  const [post, setPost] = useState(
    {}
  )

  const [countdown, setCountdown] = useState(3);


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
        post_num: text.post_num,
        total_post: text.total_post,
        post_ratio: text.post_ratio,

        user_num: text.user_num,
        total_user: text.total_user,
        user_ratio: text.user_ratio,
      });

      setPost({
        username: text.latest_post.username,
        content: text.latest_post.content,
        created_at: text.latest_post.created_at,
        url: text.latest_post.url,
        political_related: text.latest_post.political_related ? 'Yes' : 'No',
        criminal_related: text.latest_post.criminal_related ? 'Yes' : 'No',
        employment_related: text.latest_post.employment_related ? 'Yes' : 'No',
        traffic_related: text.latest_post.traffic_related ? 'Yes' : 'No',
      });
    } else {
      console.error(`Error fetching data: ${response.status}`);
    }


    setCurrentTime(new Date().toLocaleString()); // update the current time state

    };


    const updateTime = () => {

      setCountdown((prevCountdown) => (prevCountdown > 1 ? prevCountdown - 1 : 3));
    };

    const fetchDataIntervalId = setInterval(fetchData, 3000);
    const updateTimeIntervalId = setInterval(updateTime, 1000);

    return () => {
      clearInterval(fetchDataIntervalId);
      clearInterval(updateTimeIntervalId);
    };
  }, []);

  const sanitizedContent = DOMPurify.sanitize(post.content);

  

  const handleButtonClick = () => {
    window.open(post.url, '_blank', 'noopener,noreferrer');
  };

  const COLORS = ['#0088FE', '#00C49F'];
  const barChartData = [
    { name: 'Political Post', value: data.post_num },
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

      <h3>Latest post streamed</h3>
      <h4>Username</h4>
      <p>{post.username}</p>
      <h4>Content</h4>
      <div dangerouslySetInnerHTML={{ __html: sanitizedContent }}></div>

      <button onClick={handleButtonClick}>View Post</button>
      <p>Created_at: {post.created_at}</p>

      <h4>Topic information</h4>
      <p>political_related: {post.political_related}</p>
      <p>criminal_related: {post.criminal_related}</p>
      <p>employment_related: {post.employment_related}</p>
      <p>traffic_related: {post.traffic_related}</p>

      <h3>Data Summary in {data.date}</h3>
      <p>Relevant Post: {data.post_num}</p>
      <p>Total Post: {data.total_post}</p>

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
    </div>
  );
};

export default MastodonData;
