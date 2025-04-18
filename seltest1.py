import json
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup headless Chrome driver
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Extract description and assessment length from detail page
def extract_detail_info(detail_url):
    try:
        driver.get(detail_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".product-catalogue-training-calendar__row"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.select(".product-catalogue-training-calendar__row")

        description = ""
        assessment_length = ""

        for row in rows:
            heading = row.find("h4")
            para = row.find("p")
            if not heading or not para:
                continue

            heading_text = heading.get_text(strip=True).lower()
            if "description" in heading_text:
                description = para.get_text(strip=True)
            elif "assessment length" in heading_text:
                match = re.search(r"\d+", para.get_text())
                assessment_length = match.group(0) if match else ""

        return description, assessment_length
    except Exception:
        return "", ""

# Main scraping function
def scrape_all_pages(base_url):
    start = 0
    all_products = []

    while True:
        paginated_url = f"{base_url}&start={start}"
        print(f"Scraping: {paginated_url}")
        driver.get(paginated_url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
            )
        except:
            print("No more data or timed out.")
            break

        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.select("table tbody tr")[1:]

        if not rows:
            break

        for row in rows:
            try:
                title_tag = row.select_one("td.custom__table-heading__title a")
                product_title = title_tag.text.strip()
                product_link = "https://www.shl.com" + title_tag["href"]

                remote_td = row.select("td.custom__table-heading__general")[0]
                adaptive_td = row.select("td.custom__table-heading__general")[1]
                test_type_td = row.select("td.custom__table-heading__general")[2]

                remote_testing = bool(remote_td.select_one("span.catalogue__circle.-yes"))
                adaptive = bool(adaptive_td.select_one("span.catalogue__circle.-yes"))

                test_types = [span.text.strip() for span in test_type_td.select("span.product-catalogue__key")]
                test_type_str = ", ".join(test_types)

                description, assessment_length = extract_detail_info(product_link)

                product_data = {
                    "title": product_title,
                    "url": product_link,
                    "remote_testing": remote_testing,
                    "adaptive": adaptive,
                    "test_type": test_type_str,
                    "description": description,
                    "assessment_length_minutes": assessment_length
                }

                all_products.append(product_data)
            except Exception as e:
                print("Error parsing row:", e)

        start += 12
        time.sleep(1)

    return all_products

# Scrape both types
data = []
for type_val in [1, 2]:
    base_url = f"https://www.shl.com/solutions/products/product-catalog/?type={type_val}"
    data += scrape_all_pages(base_url)

driver.quit()

# Save to file
with open("shl_products.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("✅ Scraping complete. Data saved to 'shl_products.json'")
