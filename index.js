const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const TorrentSearchApi = require("torrent-search-api");
TorrentSearchApi.enableProvider("Torrent9");

let magnetLinks = [];

const getTorrent = async (name, limit = 20) => {
  try {
    const torrents = await TorrentSearchApi.search(name, "All", limit); // Limiting the search results to 'limit'

    for (const torrent of torrents) {
      const magnetLink = await TorrentSearchApi.getMagnet(torrent);
      magnetLinks.push({ title: torrent.title, magnetLink });
    }

    return magnetLinks; // Return the result of the torrent search
  } catch (error) {
    console.error("Error searching for torrents:", error);
    throw error; // Re-throw the error to be caught by the calling function
  }
};

app.use(bodyParser.json());

app.get("/", (req, res) => {
  res.status(200).json({
    success: true,
    message: "Server is Working Fine",
  });
});

app.post("/search/:id", async (req, res) => {
  const { id } = req.params; // Extract the search query from the dynamic parameter
  magnetLinks = []; // Clear the previous search results

  try {
    const result = await getTorrent(id);
    res.status(200).json({
      success: true,
      body: result,
      message: "Search completed.",
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Error searching for torrents.",
      error: error.message,
    });
  }
});

const PORT = process.env.PORT || 3000;

const server = app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

process.on("uncaughtException", (err) => {
  console.log(`Uncaught Exception error: ${err.message}`);
  process.exit(1);
});

process.on("unhandledRejection", (err) => {
  console.log(`Error by Unhandled Rejection: ${err.message}`);
  process.exit(1);
});
