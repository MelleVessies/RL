from flask import Flask,render_template, request
import numpy as np
import json
from . import main
import os
from collections import defaultdict
import time


@main.route('/', methods=['GET'])
def index():
    return render_template("base.html")

# Example of loading a page by url, preferable through ajax in js
@main.route('/example', methods=['GET'])
def example():
    return render_template("base.html")

@main.route("/getPage", methods=['GET'])
def renderPage():
    type = request.args.get('type')
    if type not in ['home', 'credits', 'blog']:
        print("invalid page")

    return render_template(type + ".html")

@main.route('/run_ajax', methods=['GET'])
def getEpisode():
    # data wil contain eps, discount, etc
    data = json.loads(request.args.get('data'))

    # return video url
    return json.dumps(["/static/videos/animation_2.mp4"])


@main.route("/list_results", methods=['GET'])
def getResultList():
    with open('results/processed_data.json', 'r') as f:
        result_list = json.load(f)
    return json.dumps(result_list)
