# Price Tracker Bot

This bot scrapes prices of products from popular ecommerce websites and sends email whenever a price drop is detected.

## Pre-requisites:
You can refer the requirements.txt file to get an idea of the libraries and technologies you may need.

## Working:
1. In this repository you will find a **server.py** file under the web_app folder which is a flask application. This application is used to take information from the user
   information such as: User name, Email, Product URL, Desired price, Product name. This information is store in an SQLite3 database.
2. Once the information has been stored the scraper.py file is run this file fetches the product URL from the database and scrapes the actual price of the product from the url.
3. This price is compared with the Desired price entered by the user which is also fetched from the database, on comparison if the actual price is less than or equal to the desired price (entered by the user), an email is sent to the user stating that a price drop has been detected.
4. The **scraper.py** file runs at regular intervals to check for any price drops in the product URLs provided by the user.
5. An added function is that there is an extra column in the database called notified which takes values between 0 and 1.
6. When an email is sent it means that a price drop has been detected.
7. To avoid sending multiple emails to a user, once the email is sent the corresponding row in the database is flagged as "1" in the notified column.
8. This ensures that a user doesn't get a mail everytime the program runs.  

## Setup:
1. Clone this repository to your local system:
```bash
git clone https://github.com/srivts/Price-Tracker-Bot.git
cd Price-Tracker-Bot
```
2. Instal required dependencies:
```bash
pip install -r requirements.txt
```
3. Run the flask application to collect input:
```bash
python web_app/server.py
```
4. Start the scraper to check for price drops and send email notifications:
```bash
python scraper.py
```
## Usage:
1. Once the Flask app is running, visit http://localhost:5000 to input your product details and email preferences.
2. The bot will then monitor the product URL and send you an email whenever the price drops to your desired value.

## Example:
1. User enters:
   - Product URL: https://www.amazon.in/dp/B08S5G1YTV (This is an example url)
   - Product name: lorem wireless earphones
   - Desired price: ₹2000
   - Name: John Doe
2. Bot scrapes the product URL and detects the price:
   - Scraped Price: ₹1,500
3. Price Comparison:
   - Scraped Price (₹1,500) is less than or equal to the Desired Price (₹2,000), so the bot sends an email to the user.

## Contributions: 
Contributions are always welcome, follow these steps to contribute:
1. Fork this repository.
2. Create a new branch: git checkout -b feature-name
3. Make your changes and commit: git commit -am 'Add new feature'
4. Push to the branch: git push origin feature-name
5. Create a pull request

## Notes:
1. Make sure you have access to an SMTP server for sending emails (e.g., Gmail, Mailgun).
2. Regular scraping can cause rate limiting on e-commerce websites. Consider implementing delays between requests to avoid being blocked.
3. You can modify the scraping logic to support more websites or specific product categories.

## License:
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

