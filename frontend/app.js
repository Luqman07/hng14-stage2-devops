const express = require("express");
const axios = require("axios");
const path = require("path");

const app = express();

const API_URL = process.env.API_URL || "http://api:8000";
const PORT = process.env.PORT || 3000;

const axiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});

app.use(express.json());
app.use(express.static(path.join(__dirname, "views")));

app.get("/health", (req, res) => {
  res.status(200).json({ status: "ok" });
});

app.post("/submit", async (req, res) => {
  try {
    const response = await axiosInstance.post("/jobs");
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get("/status/:id", async (req, res) => {
  try {
    const response = await axiosInstance.get(`/jobs/${req.params.id}`);
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Frontend running on port ${PORT}`);
});
