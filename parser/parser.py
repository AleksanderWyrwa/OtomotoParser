import requests
from bs4 import BeautifulSoup
import sqlite3
from multiprocessing import Pool, cpu_count
from flask import Flask, jsonify, request

app = Flask(__name__)

DATABASE_PATH = '/data/cars.db'

@app.route('/filter_cars', methods=['POST'])
def filter_cars():
    if request.method == 'POST':
        data = request.json
        brand = data.get('brand')

        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        query = "SELECT * FROM cars WHERE 1=1"
        if brand:
            query += f" AND brand='{brand}'"
        c.execute(query)
        filtered_cars = c.fetchall()
        conn.close()
        return jsonify(filtered_cars)

    return jsonify([])

def extract_car_data(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    cars_data = []

    car_listings = soup.find_all('article', class_='ooa-yca59n e1i3khom0')
    for car_listing in car_listings:
        car_data = {}

        title = car_listing.find('h1', class_='e1i3khom9 ooa-1ed90th er34gjf0').text.strip()
        brand = title.split()[0].lower()
        car_data['brand'] = brand

        car_data['title'] = title
        car_data['description'] = car_listing.find('p', class_='e1i3khom10 ooa-1tku07r er34gjf0').text.strip()
        details = car_listing.find_all('dd', class_='ooa-1omlbtp e1i3khom13')
        car_data['mileage'] = details[0].text.strip()
        car_data['fuel_type'] = details[1].text.strip()
        car_data['gearbox'] = details[2].text.strip()
        car_data['year'] = details[3].text.strip()
        location_info = car_listing.find_all('dd', class_='ooa-1jb4k0u e1i3khom15')
        car_data['location'] = location_info[0].text.strip()
        car_data['updated'] = location_info[1].text.strip()
        car_data['price'] = car_listing.find('h3', class_='e1i3khom16 ooa-1n2paoq er34gjf0').text.strip()
        car_data['currency'] = car_listing.find('p', class_='e1i3khom17 ooa-8vn6i7 er34gjf0').text.strip()

        car_data['car_link'] = car_listing.find('a', href=True)['href']
        car_data['photo_link'] = car_listing.find('img', class_='e17vhtca4 ooa-2zzg2s')['src']

        cars_data.append(car_data)

    return cars_data

def store_car_data(data):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS cars
                 (title TEXT, brand TEXT, description TEXT, mileage TEXT, fuel_type TEXT, gearbox TEXT, year TEXT, location TEXT, updated TEXT, price TEXT, currency TEXT, car_link TEXT, photo_link TEXT)''')

    for car in data:
        c.execute("INSERT INTO cars VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (car['title'], car['brand'], car['description'], car['mileage'], car['fuel_type'], car['gearbox'], car['year'],
                   car['location'], car['updated'], car['price'], car['currency'], car['car_link'], car['photo_link']))

    conn.commit()
    conn.close()

def fetch_data_from_page(url):
    print(f"Fetching data from {url}...")
    car_data = extract_car_data(url)
    return car_data

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    data = request.json
    base_url = data.get('base_url')
    num_pages = data.get('num_pages', 5)
    urls = [f"{base_url}?page={page}" for page in range(1, num_pages + 1)]
    with Pool(cpu_count()) as pool:
        results = pool.map(fetch_data_from_page, urls)

    all_car_data = [car for result in results for car in result]
    store_car_data(all_car_data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
