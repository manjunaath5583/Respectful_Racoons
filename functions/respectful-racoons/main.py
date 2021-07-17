import os

from flask import Flask, jsonify, make_response, request
from requests import get

app = Flask(__name__)


@app.route("/")
def hello():  # noqa: D103
    return make_response(jsonify({"message": "Hello, world!"}))


@app.get("/weather")
def get_weather():  # noqa: D103
    ip = request.args.get("ip")
    if not ip:
        return make_response(
            jsonify({"error": "Please provide an IP in the query"}), 400
        )
    res = get(
        f"https://api.weatherapi.com/v1/current.json?key={os.getenv('WEATHER_APIKEY')}&q={ip}"
    )
    return make_response(jsonify(res.json()), res.status_code)


@app.get("/news")
def get_news():
    res = get(
        "https://gnews.io/api/v4/top-headlines?max=10&lang=en&token="
        + os.getenv("NEWS_APIKEY")
    )
    return make_response(jsonify(res.json()), res.status_code)
