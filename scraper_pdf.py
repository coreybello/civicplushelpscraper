import os
import time
import json
import pdfkit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- Config ---
DATA_FOLDER = "pdf_articles"
RETRY_LIMIT = 3
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
SECTION_JSON = "section_urls.json"
os.makedirs(DATA_FOLDER, exist_ok=True)

# --- Load section URLs ---
def load_section_urls():
    with open(SECTION_JSON, "r") as f:
        return json.load(f)

# --- Extract article links using Selenium ---
def get_article_links_selenium(driver, section_url):
    driver.get(section_url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []
    for a in soup.select("a[href*='/articles/']"):
        href = a.get("href")
        if href and href.startswith("/hc/en-us/articles/"):
            full_url = "https://www.civicengagecentral.civicplus.help" + href.split("?")[0]
            if full_url not in links:
                links.append(full_url)
    return links

# --- Save article as PDF ---
def save_article_as_pdf(article_url, attempt=1):
    filename = article_url.rstrip("/").split("/")[-1]
    safe_filename = "".join(c if c.isalnum() or c in "-_" else "_" for c in filename)
    pdf_path = os.path.join(DATA_FOLDER, f"{safe_filename}.pdf")

    if os.path.exists(pdf_path):
        print(f"   ✅ Already exists: {pdf_path}")
        return

    print(f"   📄 Downloading (Attempt {attempt}): {article_url}")
    try:
        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
        pdfkit.from_url(article_url, pdf_path, configuration=config)
        print(f"   ✅ Saved: {pdf_path}")
    except Exception as e:
        print(f"   ❌ Failed to save {article_url}: {e}")
        if attempt < RETRY_LIMIT:
            time.sleep(5)
            save_article_as_pdf(article_url, attempt + 1)

# --- Main ---
def main():
    section_urls = load_section_urls()

    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Prompt for CAPTCHA
    print("🛑 Solve CAPTCHA if it appears, then press ENTER to continue...")
    driver.get("https://www.civicengagecentral.civicplus.help/hc/en-us")
    input("🔓 Press ENTER after CAPTCHA is solved...")

    for idx, section_url in enumerate(section_urls):
        print(f"\n🔍 Section: {section_url}")
        if idx == 0:
            time.sleep(10)  # Longer wait for first load

        try:
            article_links = get_article_links_selenium(driver, section_url)
            print(f"   ➤ Found {len(article_links)} article(s)")
            for article_url in article_links:
                save_article_as_pdf(article_url)
        except Exception as e:
            print(f"❌ Error processing section {section_url}: {e}")

    driver.quit()

if __name__ == "__main__":
    from bs4 import BeautifulSoup
    main()
