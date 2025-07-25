import React, { useEffect, useState, useRef } from 'react';

import '../App.css'

function GetPrice() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };


  const handleSearch = async (customQuery) => {
    const searchQuery = customQuery || query;
    try {
      const res = await fetch(`http://localhost:8000/prices/latest?symbol=${encodeURIComponent(query)}`);
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
  };
  
  const handleInputChange2 = (value) => {
    setQuery(value);
    handleSearch(value);
  };


  return (
    <div className = "get_price" style={{marginLeft: "40px", padding: "20px" }}>
      <h1 style = {{marginTop: "0px"}}>Get Most Recent Price</h1>
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
      <h2> Example Symbols </h2>

      

      <div>
          <p style = {{fontSize: "18px"}}>Tech</p>
          <button onClick={() => handleInputChange2("AAPL")} className = "aapl_button" style={{fontSize: "18px", height: "27px", marginRight: "30px"}}>AAPL: Apple</button>
          <button onClick={() => handleInputChange2("NVDA")} className = "NVDA_button" style={{fontSize: "18px", height: "27px", marginRight: "30px"}}>NVDA: Nvidia</button>
          <button onClick={() => handleInputChange2("AMZN")} style={{backgroundColor: "black", color: "gold", fontSize: "18px", height: "27px", marginRight: "30px"}}>AMZN: Amazon</button>
          <button onClick={() => handleInputChange2("MSFT")} className = "MSFT_button" style={{fontSize: "18px", height: "27px", marginRight: "30px"}}>MSFT: Microsoft</button>
          <button onClick={() => handleInputChange2("IBM")} className = "IBM_button" style={{color: "white", fontSize: "18px", height: "27px", marginRight: "30px"}}>IBM</button>
      </div>

      <div>
          <p style = {{fontSize: "18px"}}>Finance</p>
          <button onClick={() => handleInputChange2("AMJB")} style={{backgroundColor: "rosybrown", fontSize: "18px", height: "27px", marginRight: "20px"}}>AMJB: JPMorgan Chase</button>
          <button onClick={() => handleInputChange2("COF")} style={{backgroundColor: "navy", color: "white", fontSize: "18px", height: "27px", marginRight: "20px"}}>COF: Capital One</button>
          <button onClick={() => handleInputChange2("WFC")} style={{backgroundColor: "orangered", color: "gold", fontSize: "18px", height: "27px", marginRight: "20px"}}>WFC: Wells Fargo</button>
          <button onClick={() => handleInputChange2("GS")} style={{backgroundColor: "skyblue", fontSize: "18px", height: "27px", marginRight: "20px"}}>GS: Goldman Sachs</button>
      </div>
    </div>
  );
}

export default GetPrice;