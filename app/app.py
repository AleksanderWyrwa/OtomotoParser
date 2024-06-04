import requests
from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

PARSER_API_URL = "http://parser:5000" #test

def get_unique_brands():
    conn = sqlite3.connect('/data/cars.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT brand FROM cars")
    brands = c.fetchall()
    conn.close()
    return [brand[0] for brand in brands]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/filter_cars')
def filter_cars():
    brands = get_unique_brands()
    return render_template('filter_cars.html', brands=brands)

@app.route('/api/filter_cars', methods=['POST'])
def api_filter_cars():
    data = request.json
    brand = data.get('brand')

    conn = sqlite3.connect('/data/cars.db')
    c = conn.cursor()
    query = "SELECT * FROM cars WHERE 1=1"
    if brand:
        query += f" AND brand='{brand}'"
    c.execute(query)
    filtered_cars = c.fetchall()
    conn.close()
    return jsonify(filtered_cars)


@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    data = request.json
    brand = data.get('brand')
    model = data.get('model')
    base_url = f'https://www.otomoto.pl/osobowe/{brand}' + (f'/{model}' if model else '')

    num_pages_to_scrape = 5

    # Make request to parser container's API to fetch data
    response = requests.post(f"{PARSER_API_URL}/fetch_data",
                             json={"base_url": base_url, "num_pages": num_pages_to_scrape})

    if response.status_code == 200:
        if response.text == "Data fetched and stored in the database.":
            return "Data fetched and stored in the database."
        else:
            return "No data found to scrape.", 404
    else:
        return "Failed to fetch data", 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
