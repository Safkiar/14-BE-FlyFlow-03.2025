from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



def get_losers_data():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium" 
    service = Service("/usr/bin/chromedriver")  # Ścieżka do chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    
    url = "https://finance.yahoo.com/markets/stocks/losers/"
    driver.get(url)
    
    results = []
    
    try:
        # Attempt to click the "accept cookies" button if it appears
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.accept-all"))
        )
        accept_button.click()
        time.sleep(2)
    except Exception as e:
        # If the button isn't found, we continue
        pass
    
    try:
        # Wait for the table to load
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table[data-testid='table-container']"))
        )
        # Get all table rows; assuming the first row is a header row.
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows[1:]:
            # Get all cells in the row
            cells = row.find_elements(By.TAG_NAME, "td")
            # Expect at least 5 columns:
            # 0: Symbol, 1: Company Name, 2: Price, 3: Change, 4: Change %
            if len(cells) >= 5:
                trademark = cells[0].text.strip()
                company_name = cells[1].text.strip()      # Company name
                price = cells[3].text.strip()               # Price
                change_percent = cells[5].text.strip()        # Percentage change
                results.append([trademark,company_name, price, change_percent])
          
    except Exception as e:
        print("❌ Błąd podczas scrapowania:", e)
    finally:
        print(results)
        driver.quit()
        return results 
get_losers_data()