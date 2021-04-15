import os
from flask import Flask, jsonify, Response
from flask import render_template, send_file
from config import config, cache
import json
import io


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    @app.route('/env')
    def env():
        env_list = {}
        for item, value in os.environ.items():
            env_list[item] = value
        return jsonify(env_list)

    @app.route("/health")
    def health():
        return Response("OK", status=200)

    @app.route('/')
    def home():
        latest_values = json.loads(cache.get('values').decode()) if cache.get('values') else []
        return render_template('index.html', values=latest_values)

    @app.route('/values')
    def values():
        latest_values = json.loads(cache.get('values').decode()) if cache.get('values') else {}
        return jsonify(latest_values)

    @app.route('/image')
    def image():
        image = cache.get('image')
        if image:
            return send_file(io.BytesIO(image), mimetype='image/jpeg')
        else:
            return send_file('static/no_feed.jpeg', mimetype='image/jpeg')

    return app
