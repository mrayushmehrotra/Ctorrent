from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

# Get the torrent name from the user
user_input = input("Enter your torrent name: ")

# Set up Chrome options to run in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument(
    "--disable-gpu"
)  # Optional: Disable GPU acceleration (useful for headless mode)
chrome_options.add_argument(
    "--window-size=1920x1080"
)  # Set window size (optional for responsive pages)

# Initialize the WebDriver with headless option
driver = webdriver.Chrome(options=chrome_options)

# Go to the torrent website
driver.get("https://snowfl.com")

# Give the page time to load
time.sleep(2)

# Find the search input element by name
search_input = driver.find_element(By.NAME, "query")

# Enter the user input into the search box
search_input.send_keys(user_input)

# Simulate pressing the Enter key
search_input.send_keys(Keys.RETURN)

# Wait for search results to load
time.sleep(5)

# Get the page's DOM after the search results are displayed
dom = driver.page_source
soup = BeautifulSoup(dom, "html.parser")

# Extract the torrent details using the correct CSS selectors
torrent_details = soup.find_all("span", class_="name")
torrent_sizes = soup.find_all("span", class_="size")
torrent_leechers = soup.find_all("span", class_="leech")
torrent_seeders = soup.find_all("span", class_="seed")

# Extract torrent links
torrent_links = soup.find_all("a", class_="torrent")

# Print out torrent details
for i in range(len(torrent_details)):
    print(f"Torrent {i + 1}:")
    print("Name:", torrent_details[i].text)
    print("Size:", torrent_sizes[i].text if i < len(torrent_sizes) else "N/A")
    print("Seeders:", torrent_seeders[i].text if i < len(torrent_seeders) else "N/A")
    print("Leechers:", torrent_leechers[i].text if i < len(torrent_leechers) else "N/A")
    print("Link:", torrent_links[i]["href"] if i < len(torrent_links) else "N/A")
    print()

# Close the browser window
driver.quit()
