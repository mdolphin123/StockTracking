import React, { useEffect, useState, useRef } from 'react';
import axios from "axios"
import logo192 from './logo192.png'; // placeholder mock graph for now
import '../App.css'

function GetAverage() {
    const [query, setQuery] = useState("");
    const [query2, setQuery2] = useState("");
    const [response, setResponse] = useState("")
    const [imgURL, setimgURL] = useState("")


    const handleInputChange = (e) => {
        setQuery(e.target.value);
    };

    const handleInputChange2 = (e) => {
        setQuery2(e.target.value);
    };

    

    const handleSearch = async (customQuery) => {
      const searchQuery = customQuery || query;
      try {
        const res = await fetch(`http://localhost:8000/average?symbol=${encodeURIComponent(query)}`);
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        const data = await res.json();
        setResponse(data);
        console.log("Backend response:", data);
      } catch (error) {
        console.error("Error fetching data:", error);
        setResponse({ error: error.message });
      }
      handleSearch2(searchQuery)
    };

    const handleSearch2 = async (customQuery) => {
      const searchQuery2 = customQuery || query;
      try {
        const res = await fetch(`http://localhost:8000/graph?symbol=${encodeURIComponent(query)}`);
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        const blob = await res.blob(); // Get image blob
        const imageObjectURL = URL.createObjectURL(blob); // Create a URL for the blob
        setimgURL(imageObjectURL);
        console.log("Backend response:", imageObjectURL);

      } catch (error) {
        console.error("Error fetching data:", error);
        setResponse({ error: error.message });
      }
    };





  return (
    <div>
    <div className = "average_box" style={{padding: "20px" }}>
      <h1 >Get Average and Graph</h1>
      <p style = {{fontSize: "18px"}}> Gets moving average of 5 most recent updates for inputted symbol and generates graph
      </p>
      <input
        type="text"
        value={query}
        onChange={handleInputChange}
        placeholder="Enter symbol"
        style={{ fontSize: "24px", marginRight: "10px", width: "200px", height: "25px"}}
      />
      <button onClick={handleSearch} style={{marginLeft: "10px", marginTop: "20px", fontSize: "21px", height: "27px", marginBottom: "20px"}}>Search</button>
      {response && (
        <div style={{ marginTop: "20px" }}>
          <strong>Response:</strong>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
    <div className = "graph_box">        
        <img style = {{marginLeft: "200px", marginTop: "15px", width: "465px"}} src={imgURL || logo192} alt=""></img> {/* Added alt text and fallback */}
      <div/>
    </div>

    </div>
  );
}

export default GetAverage;