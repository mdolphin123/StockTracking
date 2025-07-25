import React, { useState } from "react";
import axios from "axios"
import '../App.css'



function StartPoll() {
  const [symbols, setSymbol] = useState("");
  const [interval, setInterval] = useState(60);
  const [response, setResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Split comma-separated symbols into array
    const symbolArray = symbols.split(",").map((s) => s.trim());

    try {
      const res = await axios.post("http://localhost:8000/prices/poll", {
        symbols: symbolArray,
        interval: Number(interval),
      });
      setResponse(res.data);

    } catch (error) {
      console.error("Poll failed:", error);
      setResponse({error: error.message });
    }
  };

  return (
    <div className = "get_poll">
      <h1 style = {{marginLeft: "20px", marginTop: "20px", marginBottom: "40px"}}>Poll Price Data</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label style = {{marginLeft: "20px", fontSize: "24px"}} className="block">Enter Symbols (comma-separated)</label>
          <input
            type="text"
            value={symbols}
            onChange={(e) => setSymbol(e.target.value)}
            placeholder="e.g. AAPL, IBM"
            className="border p-2 w-full"
            style={{ fontSize: "24px", marginLeft: "20px", width: "200px", height: "25px", marginBottom: "40px"}}
            required
          />
        </div>
        <div>
          <label style = {{marginLeft: "20px", fontSize: "24px", marginBottom: "40px"}} className="block">Enter Interval (seconds)</label>
          <input
            type="number"
            value={interval}
            onChange={(e) => setInterval(e.target.value)}
            className="border p-2 w-full"
            style={{ fontSize: "24px", marginLeft: "20px", width: "200px", height: "25px"}}
            required
          />
        </div>
        <button style = {{marginTop: "40px", marginLeft: "20px", fontSize: "21px"}}
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Submit
        </button>
      </form>

      {response && (
        <div style = {{marginLeft: "20px", marginTop: "40px"}}>
          <h3 className="text-lg font-semibold">Response:</h3>
          <pre className="bg-gray-100 p-2 rounded">{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};


export default StartPoll;