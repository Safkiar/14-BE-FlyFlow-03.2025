# https://finance.yahoo.com/markets/stocks/most-active/
# https://finance.yahoo.com/markets/stocks/gainers/
# https://finance.yahoo.com/markets/stocks/losers/

# https://www.investing.com/indices/germany-30 

# https://markets.businessinsider.com/index/s&p_500
# https://markets.businessinsider.com/index/nasdaq_100
# https://www.money.pl/gielda/indeksy_gpw/wig20/

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



def get_gainers_data():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = "https://finance.yahoo.com/markets/stocks/gainers/"
    driver.get(url)
    
    results = []
    
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.accept-all"))
        )
        accept_button.click()
        time.sleep(2)
    except Exception as e:
        pass
    
    try:
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table[data-testid='table-container']"))
        )
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
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