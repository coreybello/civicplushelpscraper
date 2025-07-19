# 🧾 CivicPlus Help Center Article Scraper

This Python script scrapes all article links from each section of the [CivicEngage Central Help Center](https://www.civicengagecentral.civicplus.help/hc/en-us), then downloads each article as an individual PDF file.

---

## ✅ Features

- ✅ Uses Selenium to extract dynamically loaded article links.
- 📄 Saves each article as a properly named `.pdf` file (matching the article slug).
- 🔐 Handles CAPTCHA manually on first load.
- ♻️ Includes retry logic for failed downloads (up to 3 attempts).
- ⚡ Handles lazy-loaded content and dynamic rendering.
- 🧠 Skips articles that have already been downloaded.

---

## 📁 Folder Structure

```
.
├── scraper_pdf.py          # Main scraper script
├── section_urls.json       # List of Help Center section URLs to scrape
├── pdf_articles/           # Directory where downloaded PDFs are saved
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🛠️ Prerequisites

- **Python 3.8 or later**
- Google Chrome installed
- [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) installed and added to your system PATH (see below)

---

## 📦 Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/civicplus-pdf-scraper.git
cd civicplus-pdf-scraper
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activate  # on Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)

Make sure `wkhtmltopdf.exe` is located at:

```
C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe
```

Or update the `WKHTMLTOPDF_PATH` variable in `scraper_pdf.py`.

---

## ⚙️ Usage

1. Edit `section_urls.json` with your desired CivicPlus section URLs:

```json
[
  "https://www.civicengagecentral.civicplus.help/hc/en-us/sections/360002034173-Best-Practices",
  "https://www.civicengagecentral.civicplus.help/hc/en-us/sections/360010477914-Training"
]
```

2. Run the script:

```bash
python scraper_pdf.py
```

3. A Chrome window will open.  
   🛑 **If CAPTCHA appears, solve it**, then press `ENTER` in the terminal.

---

## 🧠 How It Works

- Uses Selenium to extract article URLs from CivicPlus Help Center sections.
- Converts each article to PDF using `pdfkit` (with `wkhtmltopdf`).
- Filenames match the URL slug (e.g., `360009540273-Update-a-Widget-in-the-Footer.pdf`).
- Failed downloads retry up to 3 times.
- Output is saved in the `pdf_articles/` folder.

---

## 🐞 Troubleshooting

- **CAPTCHA won't go away**: Manually solve it and hit `ENTER` again.
- **Blank PDFs**: First page load may need extra wait time (already built in).
- **"ContentOperationNotPermittedError"**: Automatically retried.
- **Protocol errors**: Often due to dynamic elements or CSP; retries may succeed.

---

## 📜 License

MIT © 2025 Corey Bello  
Built for civic data scraping and offline documentation use.
