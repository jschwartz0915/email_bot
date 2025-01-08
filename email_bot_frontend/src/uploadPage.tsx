import React, { useState } from "react";

const uploadPage: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const [results, setResults] = useState<Array<any> | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!selectedFile) {
      setUploadStatus("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setUploadStatus("Uploading...");

      const response = await fetch("http://localhost:8000/api/send-emails", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        setUploadStatus(`Error: ${errorData.detail || "Failed to send emails."}`);
        return;
      }

      const data = await response.json();
      setUploadStatus("Emails sent successfully!");
      setResults(data.results);
    } catch (error) {
      setUploadStatus("Error: Unable to upload the file.");
      console.error("Upload error:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4">Send Emails</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label
              htmlFor="file-upload"
              className="block text-sm font-medium text-gray-700"
            >
              Upload File (CSV or Excel)
            </label>
            <input
              id="file-upload"
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={handleFileChange}
              className="mt-1 block w-full text-sm text-gray-700 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500"
            />
          </div>
          <button
            type="submit"
            className="w-full py-2 px-4 bg-green-600 text-white rounded-md shadow-md hover:bg-green-700 focus:outline-none"
          >
            Send Emails
          </button>
        </form>
        {uploadStatus && (
          <p className="mt-4 text-sm text-gray-600">{uploadStatus}</p>
        )}
        {results && (
          <div className="mt-4">
            <h2 className="text-lg font-semibold mb-2">Results:</h2>
            <ul className="space-y-2">
              {results.map((result, index) => (
                <li key={index} className="text-sm text-gray-700">
                  {result.Property_Name} ({result.Email_Address}):{" "}
                  {result.Sent ? "Sent" : "Failed"} (Status: {result.status_code})
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default uploadPage;
