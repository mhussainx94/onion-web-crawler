# 🕷️ Onion Web Crawler & Risk Analysis System

A Python-based Dark Web crawler that accesses Onion websites through the Tor network, analyzes web content, detects keywords, classifies site types, assigns risk levels, and visualizes results using a GUI.

---

## 📌 Features
- Crawls `.onion` websites using Tor
- Extracts and analyzes page content
- Detects suspicious keywords
- Classifies websites (Marketplace, Forum, etc.)
- Assigns risk levels (High, Medium, Low)
- Saves structured results in TSV format
- GUI-based result viewer using Tkinter
- HTML-based project presentation

---

## 🛠️ Technologies Used
- Python
- Tor Network
- Requests
- BeautifulSoup
- Tkinter
- HTML, CSS, JavaScript

---

## 🧠 Project Workflow
1. Input Onion URLs
2. Crawl websites via Tor proxy
3. Extract and clean content
4. Detect keywords and site type
5. Assign risk level
6. Save results
7. Visualize using GUI

---

## 📂 Project Structure

crawler.py # Main crawler logic
view.py # GUI viewer
presentation/ # HTML slides
output.tsv # Crawl results
full_pages/ # Saved page content


---

## 🚀 How to Run

### 1️⃣ Start Tor
Make sure Tor is running on port `9050`.

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt3️⃣ Run Crawler
python crawler.py

4️⃣ Run Viewer
python view.py


⚠️ Disclaimer
This project is created for educational and research purposes only.
No illegal activity is supported or encouraged.

👤 Author
Muhammad Hussain
BS Computer Science Student