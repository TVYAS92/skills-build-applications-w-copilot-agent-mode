import React, { useEffect, useState } from 'react';

const Leaderboard = () => {
  const [leaders, setLeaders] = useState([]);
  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/dashboard/leaderboard/`;

  useEffect(() => {
    fetch(apiUrl)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setLeaders(results);
        console.log('Leaderboard API endpoint:', apiUrl);
        console.log('Fetched leaderboard:', results);
      })
      .catch(err => console.error('Error fetching leaderboard:', err));
  }, [apiUrl]);

  return (
    <div className="container mt-4">
      <h2 className="mb-4 text-success">Leaderboard</h2>
      <div className="card">
        <div className="card-body">
          <table className="table table-bordered table-hover">
            <thead className="thead-dark">
              <tr>
                <th>Username</th>
                <th>Total Points</th>
              </tr>
            </thead>
            <tbody>
              {leaders.map((user, idx) => (
                <tr key={user.id || idx}>
                  <td>{user.username}</td>
                  <td>{user.total_points}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
