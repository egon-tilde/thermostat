// Stub dashboard: shows the current temperature. Only here so the folder looks like a project.
const axios = require("axios");
const _ = require("lodash");

async function show() {
  const { data } = await axios.get("/api/temperature");
  console.log(`Current: ${_.round(data.celsius, 1)} °C`);
}
show();
