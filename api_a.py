import requests
from flask import Flask, jsonify
import redis
import json

app = Flask(__name__)

cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

CACHE_TTL = 60

API_B_URL = 'http://localhost:3000/weather/'

@app.route('/recommendation/<city>', methods=['GET'])
def recommendation(city):
    city_key = city.lower()
    cached_data = cache.get(city_key)

    if cached_data:
        data = json.loads(cached_data)
        return jsonify(data)

    try:
        response = requests.get(f'http://localhost:3000/weather/{city}')
        if response.status_code != 200:
            return jsonify({"error": "City not found."}), 404

        data = response.json()
        temp = data['temp']

        if temp > 30:
            recommendation = "Drink some water and use sunscreen!"
        elif 15 <= temp <= 30:
            recommendation = "That's a nice weather! Enjoy!"
        else:
            recommendation = "It's cold! Wear a coat!"

        cache.setex(city_key, CACHE_TTL, json.dumps({
            "city": city,
            "temp": temp,
            "unit": "Celsius",
            "recommendation": recommendation
        }))

        return jsonify({
            "city": city,
            "temp": temp,
            "unit": "Celsius",
            "recommendation": recommendation
        })
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error consulting API B: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000)  
