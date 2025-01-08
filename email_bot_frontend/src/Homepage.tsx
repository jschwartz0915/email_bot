import React, { useState, useEffect } from 'react';

const HomePage = () => {
  const [stats, setStats] = useState({
    totalEmails: 0,
    successRate: 0,
    pendingEmails: 0,
  });

  const [user, setUser] = useState({
    email: '',
    firstName: '',
    lastName: '',
  });

  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserDetails = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/signed-in-user-details");

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setUser({
          email: data.email,
          firstName: data.first_name,
          lastName: data.last_name,
        });
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUserDetails();
  }, []);

  return (
    <div className="px-4 py-6">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Dashboard</h1>
      {loading ? (
        <p>Loading user details...</p>
      ) : error ? (
        <p className="text-red-500">Error: {error}</p>
      ) : (
        <div className="mb-6">
          <h2 className="text-lg font-medium text-gray-700">
            Welcome, {user.firstName} {user.lastName} ({user.email})
          </h2>
        </div>
      )}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <dt className="text-sm font-medium text-gray-500 truncate">Total Emails</dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">{stats.totalEmails}</dd>
          </div>
        </div>
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <dt className="text-sm font-medium text-gray-500 truncate">Success Rate</dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">{stats.successRate}%</dd>
          </div>
        </div>
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <dt className="text-sm font-medium text-gray-500 truncate">Pending Emails</dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">{stats.pendingEmails}</dd>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
