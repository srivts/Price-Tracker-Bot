import os
import requests
from requests.exceptions import RequestException
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait




api_key = os.getenv('SCRAPINGBEE_API_KEY')



def get_price(url):
    if 'amazon.' in url:
        return get_amazon_price(url)
    elif 'flipkart.' in url:
        return get_flipkart_price(url)
    elif 'myntra.' in url:
        return get_myntra_price(url)
    elif 'nykaa.' or 'nykaaman.' in url:
        return get_nykaa_price(url)
    else:
        print("Website not supported.")
        return None

def get_flipkart_price(url):
    response = requests.get(
            'https://app.scrapingbee.com/api/v1/',
            params={
                'api_key': api_key,
                'url': url,
                'render_js': 'true'  
            }
        )
    if response.status_code == 200:
            with open('flipkart_response.html','w', encoding='utf-8') as f:
                f.write(response.text)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                price_element = soup.select_one('div.Nx9bqj.CxhGGd')
                if price_element:
                    price_text = price_element.text
                    print(f"Raw price text from Flipkart: {price_text}")

                    price = float(re.sub(r'[^\d.]', '', price_text))
                    return price
            except Exception as e:
                print(f"An error occurred while extracting price from Flipkart: {e}")
                return None
    else:
            print(f"Failed to retrieve page from ScrapingBee: {response.status_code}")
            return None


def get_myntra_price(url):
    options=Options()
    options.headless=True
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--log-level=3") 
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:      
        driver.get(url)
        price_element=driver.find_element(By.CSS_SELECTOR, 'span.pdp-price')

        if price_element:
            price_text=price_element.text
            print(f"raw price text from myntra: {price_text}")
            price=float(re.sub(r'[^\d.]','',price_text))
            return price
        else:
            print("price element not found")
            return None
    except Exception as e:
        print(f"RequestException occured while fetching myntra price: {e} ")
        return None
    finally:
        driver.quit()



def get_amazon_price(url):
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=en-US")  

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)

        price_element = WebDriverWait(driver, 10).until(
            EC.any_of(
                EC.visibility_of_element_located(
                    (By.ID, 'priceblock_dealprice')
                ),
                EC.visibility_of_element_located(
                    (By.ID, 'priceblock_ourprice')
                ),
                EC.visibility_of_element_located(
                    (By.ID, 'priceblock_saleprice')
                ),
                EC.visibility_of_element_located(
                    (By.XPATH, '//span[@class="a-price-whole"]')
                )
            )
        )

        price_text = price_element.text
        print(f"Raw price text from Amazon: {price_text}")

        price = float(re.sub(r'[^\d.]', '', price_text))
        return price

    except TimeoutException:
        print("Failed to retrieve price from Amazon: TimeoutException")
        return None
    except NoSuchElementException:
        print("Failed to retrieve price from Amazon: NoSuchElementException")
        return None
    except Exception as e:
        print(f"An error occurred while retrieving price from Amazon: {e}")
        return None
    finally:
        driver.quit()


def get_nykaa_price(url):
    options=Options()
    options.headless=True
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--log-level=3") 
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=en-US")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:      
        driver.get(url)
        price_element=driver.find_element(By.CSS_SELECTOR, '.css-1jczs19')

        if price_element:
            price_text=price_element.text
            print(f"raw price text from nyka: {price_text}")
            price=float(re.sub(r'[^\d.]','',price_text))
            return price
        else:
            print("price element not found")
            return None
    except Exception as e:
        print(f"RequestException occured while fetching myntra price: {e} ")
        return None
    finally:
        driver.quit()

            
''' For Individual URL testing:
def main():
    url = input("Enter product URL: ").strip()
    price = get_price(url)
    if price is not None:
        print(f"The current price is ₹{price}")
    else:
        print("Could not retrieve the price.")

if __name__ == '__main__':
    main()
'''
