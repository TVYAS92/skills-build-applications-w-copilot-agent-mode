import React, { useEffect, useState } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;

  useEffect(() => {
    fetch(apiUrl)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setActivities(results);
        console.log('Activities API endpoint:', apiUrl);
        console.log('Fetched activities:', results);
      })
      .catch(err => console.error('Error fetching activities:', err));
  }, [apiUrl]);

  return (
    <div className="container mt-4">
      <h2 className="mb-4 text-primary">Activities</h2>
      <div className="card">
        <div className="card-body">
          <table className="table table-striped table-hover">
            <thead className="thead-dark">
              <tr>
                <th>Type</th>
                <th>Duration (min)</th>
                <th>Distance (km)</th>
                <th>Calories</th>
              </tr>
            </thead>
            <tbody>
              {activities.map((activity, idx) => (
                <tr key={activity.id || idx}>
                  <td>{activity.activity_type}</td>
                  <td>{activity.duration_minutes}</td>
                  <td>{activity.distance_km}</td>
                  <td>{activity.calories_burned}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Activities;
