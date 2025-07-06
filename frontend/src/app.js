import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post(
        "http://127.0.0.1:7860/analyze",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setResult(response.data);
    } catch (err) {
      console.error("Error uploading file", err);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h2>Audio Persona Profiler</h2>
      <input
        type="file"
        accept="audio/*"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleSubmit} style={{ marginLeft: "1rem" }}>
        Analyze
      </button>
      {result && (
        <div style={{ marginTop: "2rem" }}>
          <h4>Results:</h4>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
