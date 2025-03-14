import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def get_top10_changes(data):
    def parse_change(change_str):
        change_str = change_str.replace('%', '').strip().replace(',', '.')
        try:
            return float(change_str)
        except ValueError:
            return 0.0  

    sorted_data = sorted(data, key=lambda x: parse_change(x['zmiana']))
    top10_spadkow = sorted_data[:10]
    top10_wzrostow = sorted_data[-10:]
    
    return top10_wzrostow, top10_spadkow

def get_money_rankings():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.money.pl/gielda/indeksy_gpw/wig/"
    driver.get(url)
    
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'AKCEPTUJĘ I PRZECHODZĘ DO SERWISU')]"))
        )
        accept_button.click()
        print("✅ Kliknięto przycisk akceptacji cookies!")
    except Exception as e:
        print("❌ Nie udało się znaleźć/kliknąć przycisku akceptacji cookies. Kontynuujemy...")

    try:
        wait = WebDriverWait(driver, 10)
        initial_rows = len(driver.find_elements(By.CSS_SELECTOR, "div.rt-tr-group"))
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(3)
        buttons = driver.find_elements(By.CLASS_NAME, "sc-143eo0d-0")
        
        if buttons:
            button = buttons[0]
            driver.execute_script("arguments[0].click();", button)
            print("✅ Kliknięto przycisk!")
            time.sleep(3)
        else:
            print("❌ Nie znaleziono żadnych przycisków.")
        
        # Poczekaj na załadowanie nowych danych
        wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "div.rt-tr-group")) > initial_rows)
        print("✅ Nowe dane zostały załadowane.")
    except Exception as e:
        print(f"❌ Błąd podczas kliknięcia przycisku lub oczekiwania: {e}")
    
    # Pobranie źródła strony i zamknięcie drivera
    html = driver.page_source
    driver.quit()

    # Parsowanie HTML za pomocą BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    table_div = soup.find('div', class_='rt-table')
    data = []

    if table_div:
        row_groups = table_div.find_all('div', class_='rt-tr-group')
        for group in row_groups:
            rows = group.find_all('div', class_='rt-tr')
            for row in rows:
                columns = row.find_all('div', class_='rt-td')
                if len(columns) >= 3:
                    record = {
                        'nazwa': columns[0].get_text(strip=True),
                        'cena': columns[1].get_text(strip=True),
                        'zmiana': columns[2].get_text(strip=True)
                    }
                    data.append(record)
    else:
        print("Nie znaleziono elementu z klasą 'rt-table'")

    # Używamy funkcji sortującej, by uzyskać top 10 wzrostów i spadków
    return get_top10_changes(data)