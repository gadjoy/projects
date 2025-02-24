import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { GoogleMap, LoadScript, DirectionsRenderer } from "@react-google-maps/api";

const mapContainerStyle = { width: "100%", height: "400px" };
const center = { lat: 20.5937, lng: 78.9629 }; // Default center (India)

function App() {
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");
  const [trafficData, setTrafficData] = useState(null);
  const [directions, setDirections] = useState(null);

  const [mapInstance, setMapInstance] = useState(null);
  const [center, setCenter] = useState({ lat: 13.0827, lng: 80.2707 });
  const [zoom, setZoom] = useState(10);

  const GOOGLE_MAPS_API_KEY = "";

  const fetchTrafficData = async () => {
    if (!source || !destination) return alert("Enter both source and destination!");

    try {
      const response = await fetch(`http://127.0.0.1:8000/traffic_slots/?source=${source}&destination=${destination}`);
      const data = await response.json();
      
      if (!data || !data.traffic_slots || data.traffic_slots.length === 0) {
        alert("No traffic data available.");
        return;
      }

      // Transform data for Recharts
      const formattedData = data.traffic_slots.map((slot) => ({
        timeRange: slot.slot_time_range,  // X-axis (Time Slot)
        travelTime: slot.travel_time_in_minutes, // Y-axis (Travel Time)
      }));

      setTrafficData(formattedData);

      // Fetch Google Maps Directions
      const directionsService = new google.maps.DirectionsService();
      directionsService.route(
        {
          origin: source,
          destination: destination,
          travelMode: google.maps.TravelMode.DRIVING,
        },
        (result, status) => {
          if (status === "OK") setDirections(result);
        }
      );
    } catch (error) {
      console.error("Error fetching traffic data:", error);
    }
  };

  return (
    <div className="app-container">
      <h1>🚗 Quick Reach Traffic Analyzer</h1>
      <div className="input-container">
        <input type="text" placeholder="Enter Source" value={source} onChange={(e) => setSource(e.target.value)} />
        <input type="text" placeholder="Enter Destination" value={destination} onChange={(e) => setDestination(e.target.value)} />
        <button onClick={fetchTrafficData}>Check Traffic</button>
      </div>

      {/* Google Maps */}
      <LoadScript googleMapsApiKey="AIzaSyCE3XCHoxVKC_Dv2UhxI0x6id2MwVy0E2g">
        <GoogleMap mapContainerStyle={mapContainerStyle} center={center} zoom={5}>
          {directions && <DirectionsRenderer directions={directions} />}
        </GoogleMap>
      </LoadScript>

      {/* Traffic Data Graph */}
      {trafficData && trafficData.length > 0 && (
        <div className="graph-container">
          <h2>📊 Travel Time Analysis</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trafficData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timeRange" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="travelTime" stroke="#82ca9d" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

export default App;
