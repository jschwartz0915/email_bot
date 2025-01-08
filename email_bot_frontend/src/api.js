import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

export const fetchStatistics = () => axios.get(`${API_BASE_URL}/statistics`);

// Upload file using fetch
export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append("file", file); // Append file to formData

  return fetch(`${API_BASE_URL}/send-emails`, {
    method: "POST",
    body: formData,  // Send formData directly as body
    // Do not set Content-Type; browser will automatically set it
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();  // Return the JSON response
    })
    .catch((error) => {
      console.error("Error uploading file:", error);
      throw error;
    });
};


export const fetchEmailResponses = () =>
  axios.get(`${API_BASE_URL}/email-responses`, { withCredentials: true });

