import React, { useState } from "react";
import { GoogleMap, LoadScript, DirectionsRenderer, Marker } from "@react-google-maps/api";
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import {
  Box,
  TextField,
  Button,
  Typography,
  Grid,
  CircularProgress,
  Paper,
} from "@mui/material";
import axios from "axios";

const SLOT_TYPE = "SLOT";

const DraggableSlot = ({ slot }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: SLOT_TYPE,
    item: { slot },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));

  return (
    <Paper
      ref={drag}
      elevation={2}
      sx={{
        padding: 2,
        marginBottom: 2,
        backgroundColor: isDragging ? "primary.light" : "background.paper",
        borderRadius: 2,
        cursor: "grab",
        opacity: isDragging ? 0.7 : 1,
        transition: "opacity 0.2s",
      }}
    >
      <Typography variant="body1" sx={{ fontWeight: "bold" }}>
        {slot.slot_time_range}
      </Typography>
      <Typography variant="body2">Travel Time: {slot.estimated_travel_time} mins</Typography>
      <Typography variant="body2">Traffic Level: {slot.traffic_level}</Typography>
      <Typography variant="body2">Distance: {slot.distance} km</Typography>
    </Paper>
  );
};

const DroppableArea = ({ title, onDrop, slot }) => {
  const [{ isOver }, drop] = useDrop(() => ({
    accept: SLOT_TYPE,
    drop: (item) => onDrop(item.slot),
    collect: (monitor) => ({
      isOver: monitor.isOver(),
    }),
  }));

  return (
    <Paper
      ref={drop}
      elevation={3}
      sx={{
        padding: 3,
        textAlign: "center",
        backgroundColor: isOver ? "primary.light" : "background.default",
        border: "2px dashed",
        borderColor: isOver ? "primary.main" : "grey.400",
        borderRadius: 2,
        minHeight: "120px", // Consistent height to avoid shrinking
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transition: "background-color 0.3s",
      }}
    >
      {slot ? (
        <>
          <Typography variant="h6">{title}</Typography>
          <Typography variant="body1" sx={{ marginTop: 1 }}>
            {slot.slot_time_range}
          </Typography>
          <Typography variant="body2">Distance: {slot.distance} km</Typography>
        </>
      ) : (
        <Typography variant="body2" color="textSecondary">
          Drop a slot here
        </Typography>
      )}
    </Paper>
  );
};

const App = () => {
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");
  const [trafficData, setTrafficData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [toSlot, setToSlot] = useState(null);
  const [fromSlot, setFromSlot] = useState(null);
  const [directions, setDirections] = useState(null);
  const [mapInstance, setMapInstance] = useState(null);
  const [center, setCenter] = useState({ lat: 13.0827, lng: 80.2707 });
  const [zoom, setZoom] = useState(10);

  const GOOGLE_MAPS_API_KEY = "";

  const fetchTrafficData = async () => {
    if (!source || !destination) {
      setError("Please fill in both source and destination.");
      return;
    }

    setTrafficData(null);
    setToSlot(null);
    setFromSlot(null);
    setError("");
    setDirections(null);
    setLoading(true);

    if (mapInstance) {
      const markers = mapInstance.markers || [];
      markers.forEach((marker) => marker.setMap(null));
      mapInstance.markers = [];
    }

    try {
      const response = await axios.get("http://127.0.0.1:8000/traffic_slots/", {
        params: { source, destination },
      });
      setTrafficData(response.data);

      const directionsService = new window.google.maps.DirectionsService();
      directionsService.route(
        {
          origin: source,
          destination: destination,
          travelMode: window.google.maps.TravelMode.DRIVING,
        },
        (result, status) => {
          if (status === "OK") {
            setDirections(result);
          } else {
            setError("Could not fetch directions.");
          }
        }
      );

      const sourceCoords = {
        lat: parseFloat(source.split(",")[0]),
        lng: parseFloat(source.split(",")[1]),
      };
      const destinationCoords = {
        lat: parseFloat(destination.split(",")[0]),
        lng: parseFloat(destination.split(",")[1]),
      };

      const midPoint = {
        lat: (sourceCoords.lat + destinationCoords.lat) / 2,
        lng: (sourceCoords.lng + destinationCoords.lng) / 2,
      };
      setCenter(midPoint);
    } catch (err) {
      setError("Failed to fetch traffic data.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <Box sx={{ padding: 4, backgroundColor: "grey.100", minHeight: "100vh" }}>
        <Box
          sx={{
            padding: 3,
            backgroundColor: "primary.main",
            color: "white",
            borderRadius: 2,
            marginBottom: 4,
            textAlign: "center",
          }}
        >
          <Typography variant="h4">Quick Reach</Typography>
          <Typography variant="subtitle1">
            Plan your journey with optimized traffic insights.
          </Typography>
        </Box>

        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Box sx={{ marginBottom: 2 }}>
              <TextField
                fullWidth
                label="Source"
                value={source}
                onChange={(e) => setSource(e.target.value)}
                variant="outlined"
                sx={{ marginBottom: 2 }}
              />
              <TextField
                fullWidth
                label="Destination"
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                variant="outlined"
                sx={{ marginBottom: 2 }}
              />
              <Button
                fullWidth
                variant="contained"
                onClick={fetchTrafficData}
                disabled={loading}
                color="primary"
              >
                {loading ? <CircularProgress size={24} color="inherit" /> : "Get Traffic Slots"}
              </Button>
              {error && <Typography color="error" sx={{ marginTop: 2 }}>{error}</Typography>}
            </Box>

            {trafficData && (
              <>
                <Typography variant="h6" sx={{ marginBottom: 2 }}>
                  Shortest Travel Slots
                </Typography>
                {trafficData.shortest_slots.map((slot, idx) => (
                  <DraggableSlot key={idx} slot={slot} />
                ))}
                <Typography variant="h6" sx={{ marginBottom: 2, marginTop: 4 }}>
                  Longest Travel Slots
                </Typography>
                {trafficData.longest_slots.map((slot, idx) => (
                  <DraggableSlot key={idx} slot={slot} />
                ))}
              </>
            )}
          </Grid>

          <Grid item xs={12} md={8}>
            <Box sx={{ marginBottom: 4 }}>
              <LoadScript googleMapsApiKey={GOOGLE_MAPS_API_KEY}>
                <GoogleMap
                  center={center}
                  zoom={zoom}
                  mapContainerStyle={{
                    width: "100%",
                    height: "500px",
                    borderRadius: "8px",
                  }}
                  onLoad={(map) => {
                    setMapInstance(map);
                    map.markers = [];
                  }}
                >
                  {source && destination && (
                    <>
                      <Marker
                        position={{
                          lat: parseFloat(source.split(",")[0]),
                          lng: parseFloat(source.split(",")[1]),
                        }}
                      />
                      <Marker
                        position={{
                          lat: parseFloat(destination.split(",")[0]),
                          lng: parseFloat(destination.split(",")[1]),
                        }}
                      />
                    </>
                  )}
                  {directions && <DirectionsRenderer directions={directions} />}
                </GoogleMap>
              </LoadScript>
            </Box>

            <Grid container spacing={4}>
              <Grid item xs={6}>
                <DroppableArea title="From Journey" onDrop={setFromSlot} slot={fromSlot} />
              </Grid>
              <Grid item xs={6}>
                <DroppableArea title="To Journey" onDrop={setToSlot} slot={toSlot} />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Box>
    </DndProvider>
  );
};

export default App;
