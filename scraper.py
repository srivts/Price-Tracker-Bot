import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from scrapper2 import get_myntra_price, get_flipkart_price, get_amazon_price, get_nykaa_price

def send_email(user_email, product_name, actual_price, url, id):
    try:
        from_email="enter_your_email"
        app_password="enter_your_password"

        subject=f"Price drop alert!!!: {product_name}"
        body=f"The price of the product you're looking to buy has dropped to ₹{actual_price}. Go ahead and buy it before the price hikes at: {url}"

        message=MIMEMultipart()
        message["From"]=from_email
        message["To"]=user_email
        message["Subject"]=subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()   
            server.login(from_email, app_password)
            text= message.as_string()
            server.sendmail(from_email, user_email, text)
            print(f"email sent to {user_email}")

            conn=connect_to_db()
            cursor=conn.cursor()
            cursor.execute("UPDATE products SET notified=1 WHERE id=?",(id,))
            conn.commit()
            conn.close()
    except Exception as e:
        print(f"Failed to send email {e}")



def connect_to_db():
    return sqlite3.connect('product_data.db')

def get_urls():
    conn=connect_to_db()
    cursor=conn.cursor()
    cursor.execute("SELECT id, product_name, email, url, desired_price, notified FROM products")
    urls=cursor.fetchall()
    conn.close()
    return urls


api_key = os.getenv('SCRAPINGBEE_API_KEY')

def get_price(url):
    # Determine the website from URL
    if 'flipkart.' in url:
        return get_flipkart_price(url)
    elif 'amazon.' in url:
        return get_amazon_price(url)
    elif 'myntra.' in url:
        return get_myntra_price(url)
    elif 'nykaa.' or 'nykaaman.' in url:
        return get_nykaa_price(url)
    else:
        print("Website not supported.")
        return None


    
        

def main():
    urls=get_urls()
    for product in urls:
        id, name, email, url, desired_price, notified=product
        if notified==0:
            print(f"checking price for url:{name} at {url}")
            actual_price=get_price(url)
            if actual_price is not None:
                print(f"price for {url} is ₹{actual_price}")
                if actual_price<=float(desired_price):
                    print(f"price has dropped, sending email to {email}")
                    send_email(email, name, actual_price, url, id)
                else:
                    print(f"price is higher than desired price, no email sent")
            else:
                print(f"could not retrieve price for {url}")
        else:
            print(f"product {name} has already been notified, skipping")        
                
if __name__ == '__main__':
    main()
