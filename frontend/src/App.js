import React, { useState } from "react";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from "react-leaflet";
import polyline from "@mapbox/polyline";
import './App.css';

// Component to dynamically update the map's center
const MapView = ({ center }) => {
  const map = useMap();
  map.setView(center, 13);
  return null;
};

const App = () => {
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [route, setRoute] = useState(null);
  const [traffic, setTraffic] = useState(null);

  const fetchRoute = async () => {
    try {
      const routeResponse = await axios.post("http://127.0.0.1:5000/api/routing", { start, end });
      setRoute(routeResponse.data);

      const trafficResponse = await axios.post("http://127.0.0.1:5000/api/traffic", {
        time_of_day: new Date().getHours(),
      });
      setTraffic(trafficResponse.data.predicted_traffic);
    } catch (error) {
      console.error("Error fetching data:", error);
      alert("Unable to fetch route or traffic data. Please try again.");
    }
  };

  return (
    <div class="main">
      <h1>Traffic Route Planner</h1>
      <div class="box">
        <input class="input1"
          type="text"
          placeholder="Start Location"
          value={start}
          onChange={(e) => setStart(e.target.value)}
        />
        <input class="input2"
          type="text"
          placeholder="End Location"
          value={end}
          onChange={(e) => setEnd(e.target.value)}
        />
        <button onClick={fetchRoute}>Find Route</button>
      </div>

      {route && (
        <div class="details">
          <h2>Route Details</h2>
          <p><strong>Start:</strong> {route.start}</p>
          <p><strong>End:</strong> {route.end}</p>
          <p><strong>Distance:</strong> {route.distance} km</p>
          <p><strong>Duration:</strong> {route.duration} minutes</p>
        </div>
      )}

      {traffic && (
        <div class="prediction">
          <h2>Traffic Prediction</h2>
          <p><strong>Predicted Traffic Level:</strong> {traffic}</p>
          {traffic === "High" && <p style={{ color: "red" }}>Expect delays due to heavy traffic.</p>}
          {traffic === "Moderate" && <p style={{ color: "orange" }}>Plan accordingly; moderate traffic.</p>}
          {traffic === "Low" && <p style={{ color: "green" }}>Smooth driving conditions.</p>}
        </div>
      )}

      <MapContainer center={[49.41461, 8.681495]} zoom={13} style={{ height: "500px", width: "90%" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {route && (
          <>
            <MapView center={polyline.decode(route.geometry)[0]} />
            <Marker position={polyline.decode(route.geometry)[0]}>
              <Popup>Start: {route.start}</Popup>
            </Marker>
            <Marker position={polyline.decode(route.geometry).slice(-1)[0]}>
              <Popup>End: {route.end}</Popup>
            </Marker>
            <Polyline
              positions={polyline.decode(route.geometry)}
              color={traffic === "High" ? "red" : traffic === "Moderate" ? "orange" : "green"}
              weight={5}
            />
          </>
        )}
      </MapContainer>
    </div>
  );
};

export default App;
