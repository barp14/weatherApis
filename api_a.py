import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/recommendation/<city>', methods=['GET'])
def recommendation(city):
    try:
        response = requests.get(f'http://localhost:3000/weather/{city}')
        data = response.json()

        temp = data['temp']

        if temp > 30:
            recommendation = "Drink some water and use sunscreen!"
        elif 15 <= temp <= 30:
            recommendation = "That's a nice weather! Enjoy!"
        else:
            recommendation = "It's cold! Wear a coat!"

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
