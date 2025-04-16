from flask import Flask, jsonify
from random import randint

app = Flask(__name__)

@app.route('/weather/<city>', methods=['GET'])
def weather(city):
    cities = [
        "SP",
        "RJ",
        "BH",
        "CWB",
        "POA",
        "BSB"
    ]

    if city not in cities:
        return jsonify({"error": "City not found."}), 404

    temp = randint(5, 40)

    return jsonify({
        "city": city,
        "temp": temp,
        "unit": "Celsius"
    })

if __name__ == '__main__':
    app.run(port=3000)
