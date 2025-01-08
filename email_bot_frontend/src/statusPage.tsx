import React, { useEffect, useState } from "react";

const EmailResponses = () => {
  const [emailResponses, setEmailResponses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    email: "",
    propertyName: "",
  });

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value,
    }));
  };

  useEffect(() => {
    const fetchEmailResponses = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/email-responses");

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setEmailResponses(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchEmailResponses();
  }, []);

  const filteredResponses = emailResponses.filter((response) => {
    return (
      response.email.toLowerCase().includes(filters.email.toLowerCase()) &&
      response.property_name.toLowerCase().includes(filters.propertyName.toLowerCase())
    );
  });

  if (loading) return <p className="text-center text-gray-600">Loading...</p>;
  if (error) return <p className="text-center text-red-600">Error: {error}</p>;

  return (
    <div className="flex p-4 space-x-4">
      {/* Filter Sidebar */}
      <div className="w-1/4 bg-gray-100 p-4 rounded-lg shadow-md">
        <div className="mb-4">
          <button className="w-full text-left text-lg font-semibold text-gray-700">
            Filters
          </button>
          <div className="space-y-4 mt-2">
            {/* Filter by Email */}
            <div>
              <label className="block text-sm text-gray-600">Filter by Email</label>
              <input
                type="text"
                name="email"
                value={filters.email}
                onChange={handleFilterChange}
                className="mt-1 p-2 w-full border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Filter by Property Name */}
            <div>
              <label className="block text-sm text-gray-600">Filter by Property Name</label>
              <input
                type="text"
                name="propertyName"
                value={filters.propertyName}
                onChange={handleFilterChange}
                className="mt-1 p-2 w-full border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="w-3/4">
        <h1 className="text-3xl font-semibold text-gray-800 mb-4">Email Responses</h1>
        {filteredResponses.length === 0 ? (
          <p>No email responses available with the applied filters.</p>
        ) : (
          <div className="overflow-x-auto rounded-lg shadow-md">
            <table className="min-w-full bg-white border-collapse">
              <thead>
                <tr className="text-left bg-blue-100 text-gray-700">
                  <th className="px-4 py-3 border-b font-medium">Property Name</th>
                  <th className="px-4 py-3 border-b font-medium">Email</th>
                  <th className="px-4 py-3 border-b font-medium">Responded</th>
                  <th className="px-4 py-3 border-b font-medium">Emails Sent</th>
                </tr>
              </thead>
              <tbody>
                {filteredResponses.map((response, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-4 py-3 border-b text-gray-700">{response.property_name}</td>
                    <td className="px-4 py-3 border-b text-gray-700">{response.email}</td>
                    <td className="px-4 py-3 border-b text-gray-700">{response.responded ? "Yes" : "No"}</td>
                    <td className="px-4 py-3 border-b text-gray-700">{response.emails}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default EmailResponses;
